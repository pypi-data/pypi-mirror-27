'''
Copyright (c) 2017 [Chun-Pai Yang]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
'''

import os
import json

from datetime import datetime
import re
from dateutil.rrule import rrule, DAILY

class NotSupportYearException(Exception):
    pass

class DataReader:
    """ read data/{year}.holiday and pre-process it

    The usage of this class:
        data = DataReader('2017').data

    You can inherit this class like StockDataReader

    Attributes:
        _year (int): the data year
        _data (dict): the json file content

    """
    def __init__(self, year):
        self._year = year

    @property
    def data(self):
        """dict: call _getOpenFilePath() and _preProcess() to return dict data"""
        if not hasattr(self, "_data"):
            open_file = self._getOpenFilePath()
            if not os.path.isfile(open_file):
                raise NotSupportYearException("Error: not support year, file={} not exist", open_file)
            with open(open_file) as data_file:
                data = json.loads(data_file.read())
                data = self._preProcess(data)

            self._data = data
        return self._data

    @staticmethod
    def _parseDtRange(strDtRange, year):
        dtRange = []
        m = re.match("([\d]{4})-([\d]{4})", strDtRange)
        if m:
            b = m.groups()[0]
            e = m.groups()[1]
            dtstart = datetime.strptime(str(year) + b, "%Y%m%d")
            dtuntil = datetime.strptime(str(year) + e, "%Y%m%d")
            dtRange = [dtstart, dtuntil]

        return dtRange

    @staticmethod
    def _assignValue(data, year, strDt, value):
        """ assign data[strDt] = value, but strDt may be range format(i.e. '0401-0405') need to parse first """
        dtRange = DataReader._parseDtRange(strDt, year)
        if dtRange:
            for dt in rrule(DAILY, dtstart=dtRange[0], until=dtRange[1]):
                data[dt.strftime("%m%d")] = value
        else:
            data[strDt] = value

    def _preProcess(self, data):
        # do pre-process for data

        _data = {}
        for key, value in data.items():
            dtRange = DataReader._parseDtRange(key, self._year)
            if not dtRange:
                _data[key] = value
            else:
                for dt in rrule(DAILY, dtstart=dtRange[0], until=dtRange[1]):
                    _data[dt.strftime("%m%d")] = value

        return _data

    def _getOpenFilePath(self):
        # acoording self._year to get full file path

        this_dir, this_filename = os.path.split(__file__)
        if not this_dir:
            this_dir = "."
        open_file = "{}/data/{}.holiday".format(this_dir, self._year)

        return open_file


class HolidayDataReader(DataReader):
    pass


class StockDataReader(DataReader):
    # parse 'stock_close' information and add information into data
    def _extraProcess(func):
        def _retFunc(self, data):
            _data = func(self, data)
            if "stock_close" in _data:
                extra_close_days_items = _data["stock_close"]
                if isinstance(extra_close_days_items, list):
                    for item in extra_close_days_items:
                        DataReader._assignValue(_data, self._year, item, True)
                else:
                    item = extra_close_days_items
                    DataReader._assignValue(_data, self._year, item, True)

            return _data
        return _retFunc

    @_extraProcess
    def _preProcess(self, data):
        return super()._preProcess(data)


def isDay(strDt, DataReader):
    """
    This is function is core of 'holiday.isDay()' and 'stock_close.isDay()'

    Args:
        strDt: datetime str (e.g. '20171104')

    Returns:
        bool: DataReader.data[date]

    Raises:
        NotSupportYearException: Raises an exception if "data/{year}.holiday not exist"
    """
    dt = datetime.strptime(strDt, "%Y%m%d")
    query_str = "{:02d}{:02d}".format(dt.month, dt.day)

    data = DataReader(dt.year).data

    if query_str in data:
        return data[query_str]

    if dt.weekday() == 5 or dt.weekday() == 6:
        return True

    return False

