__author__ = 'Dennis'

import mysql.connector
import sys
import urllib.request
import re
import ystockquote
import datetime

db = mysql.connector.connect(host="localhost", # your host, usually localhost
                     user="chenq", # your username
                      passwd="admin", # your password
                      db="test") # name of the data base

cur = db.cursor()
cur.execute("select symbol from stock_symbol")
rows = cur.fetchall()
start_date = (datetime.datetime.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
print (start_date)
end_date = datetime.datetime.today().strftime('%Y-%m-%d')
print(end_date)
for (symbol,) in rows:
    data = ystockquote.get_historical_prices(symbol, start_date, end_date)
    for (date, dailyData) in data.items():
        print(date)
        for (key, value) in dailyData.items():
            print(symbol + " " + key + " " + value)
cur.close()
db.close()