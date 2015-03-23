__author__ = 'Dennis'

import mysql.connector
import sys
import urllib.request
import re
#import ystockquote
import datetime
import json
from threading import Thread
import YahooFinance

from csv import DictWriter
dicts = json.loads(data)
the_file = open("sample.csv", "w")
writer = DictWriter(the_file, dicts[0].keys())
writer.writeheader()
writer.writerows(dicts)
the_file.close()

gmap = {}

def requestThread(symbol):
    yahooFinanceUrl = "http://finance.yahoo.com/1?s=" + symbol
    regex = '<span id="yfs_184_' + symbol.lower() + '>(.+?</span>'
    htmlText = urllib.request.urlopen(yahooFinanceUrl).read()
    results = re.findall(re.compile(regex), htmlText)
    try:
        gmap[symbol] = results[0]
    except:
        print("got an error")


urls = "http://google.com http://cnn.com".split()
threadList = []
for url in urls:
    t = Thread(target=requestThread, args=(url,))
    t.start()
    threadList.append(t)
for b in threadList:
        b.join()

db = mysql.connector.connect(host="localhost", # your host, usually localhost
                     user="chenq", # your username
                      passwd="admin", # your password
                      db="test") # name of the data base

for key in gmap.keys():
    query = "insert into stock_symbol (symbol, last) values(" + "'" + key + "'," + gmap[key] + ")"
    cur = db.cursor()
    cur.execute(query)
    symbolList = cur.fetchall()


#read tickers from txt file
# symbolList = open("symbols.txt").read()
# symbolList = symbolList.split("\n")

# db = mysql.connector.connect(host="localhost", # your host, usually localhost
#                      user="chenq", # your username
#                       passwd="admin", # your password
#                       db="test") # name of the data base
#
# cur = db.cursor()
# cur.execute("select symbol from stock_symbol")
# symbolList = cur.fetchall()
# start_date = (datetime.datetime.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
# print (start_date)
# end_date = datetime.datetime.today().strftime('%Y-%m-%d')
# print(end_date)
#
# for (symbol,) in symbolList:
#     #htmlText = urllib.urlopen("http://www.bloomberg.com/markets/chart/data/1D/" + symbol + ":US")
#     #data = json.load(htmlText)
#     #datapoint = data["data_values"]
#     #for point in datapoints:
#     #   print "symbol", symbol, "time", point[0], "price", point[1]
#
#     #myFile = open("stock_price/daily_prices/" + symbol + ".txt", "a"
#     #for point in datapoints:
#     #   myFile.write(str(symbol + "," + str(point[0] + "," + str(point[1] + "\n")))
#     #myFile.close()
#
#     data = ystockquote.get_historical_prices(symbol, start_date, end_date)
#     for (date, dailyData) in data.items():
#         print(date)
#         for (key, value) in dailyData.items():
#             print(symbol + " " + key + " " + value)
# cur.close()
# db.close()