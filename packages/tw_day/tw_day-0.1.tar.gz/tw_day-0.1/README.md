# tw_day
----
## What is tw_day ?
A python package which help your program to decide whether the day is Taiwan holiday or Taiwan stock close day

----
## Install
pip install .

----
## Usage
    from tw_day import stock_close
    from tw_day import holiday

    day='20170125'
    if stock_close.isDay(day):
        print ("{} is stock close day".format(day))

    if holiday.isDay(day):
        print ("{} is holiday".format(day))

## How this work
Manual grep [twse](http://www.twse.com.tw/holidaySchedule/holidaySchedule.html?queryYear=91) and write information into data/{year}.holiday json file


## Note
- Only support from *2002* to *2018*
- Only support *python3*


----
## Changelog
- 2017/12/09 first version

