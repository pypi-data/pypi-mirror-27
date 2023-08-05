
import stock_close
import holiday
import sys

def test(day):
    print ("stock_close={}".format(stock_close.isDay(day)))
    print ("holiday={}".format(holiday.isDay(day)))


test(sys.argv[1])
