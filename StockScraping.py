__author__ = 'Dennis'

import mysql.connector
import sys
import urllib.request
import re
import ystockquote

db = mysql.connector.connect(host="localhost", # your host, usually localhost
                     user="chenq", # your username
                      passwd="admin", # your password
                      db="stock") # name of the data base

cur = db.cursor()
cur.execute("select symbol from stocksymbol")
rows = cur.fetchall()
for (symbol,) in rows:
    print(ystockquote.get_price(symbol))

#print(ystockquote.get_all('GOOG'))
#print(ystockquote.get_historical_prices('GOOG', '2015-01-01', '2015-02-01'))

data = ystockquote.get_historical_prices('GOOG', '2015-01-01', '2015-02-01')
for (date, dailyData) in data.items():
    print(date)
    for (key, value) in dailyData.items():
        print(key + " " + value)
cur.close()
db.close()