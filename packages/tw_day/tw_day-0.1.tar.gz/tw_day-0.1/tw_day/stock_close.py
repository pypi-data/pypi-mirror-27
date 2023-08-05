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

from tw_day import core

# is tw stock market close day
def isDay(strDt):
    """
    This is function return 'taiwan stock market is close or not' information

    Args:
        strDt: datetime str (e.g. '20171104')

    Returns:
        true: market close
        false: market open

    Raises:
        NotSupportYearException: Raises an exception if file data/{year}_holiday not exist
    """
    return core.isDay(strDt, core.StockDataReader)


if __name__ == '__main__':
    print (isDay('20170125'))
