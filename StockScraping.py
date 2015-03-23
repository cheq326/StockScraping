import os
import mysql.connector
import sys
import urllib.request
import re
import datetime
import json
from threading import Thread
import YahooFinance
import json

gmap = {}

def ensure_dir(f):
    # d = os.path.dirname(f)
    if not os.path.exists(f):
        os.makedirs(f)

def make_filename(ticker_symbol, directory):
    ensure_dir(directory)
    return directory + "/" + ticker_symbol + ".csv"

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


db = mysql.connector.connect(host="localhost", # your host, usually localhost
                     user="chenq", # your username
                      passwd="admin", # your password
                      db="stock") # name of the data base

for key in gmap.keys():
    query = "insert into stock_symbol (symbol, last) values(" + "'" + key + "'," + gmap[key] + ")"
    cur = db.cursor()
    cur.execute(query)
    symbolList = cur.fetchall()

cur = db.cursor()
cur.execute("select symbol from stock_symbol")
symbolList = cur.fetchall()
start_date = (datetime.datetime.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
# print (start_date)
end_date = datetime.datetime.today().strftime('%Y-%m-%d')
# print(end_date)
data = YahooFinance._request_yahoo('test')
# print(data)
# print(json.loads(data)["query"]["results"]["quote"])

json_data = json.loads(data)

result_count = json_data["query"]["count"]
query_date = json_data["query"]["created"]
print(result_count)
print(query_date)
cursor = db.cursor()
for quote in json_data["query"]["results"]["quote"]:
    content = ""
    for key in quote:
        if str(key) != 'symbol':
            print(str(key) + ": " + str(quote[key]))
            content = content + str(key) + ":" + str(quote[key]) + "\n"
            columns = "'" + "', '".join(quote.keys())
            placeholders = ':'+', :'.join(quote.keys())
    outfile = open(make_filename(quote["Symbol"], "D:\StockData\\" + datetime.datetime.today().strftime('%Y-%m-%d')), "w")
    outfile.write(content)
    outfile.close()

    # query = 'INSERT INTO stock_data (%s) VALUES (%s)' % (columns + "'", placeholders)
    # print(query)
    # cur.execute(query, quote)

        # variable_1 = "HELLO"
        # variable_2 = "ADIOS"
        # varlist = [variable_1,variable_2]
        # var_string = ', '.join('?' * len(varlist))
        # query_string = 'INSERT INTO table VALUES (%s);' % var_string
        # cursor.execute(query_string, varlist)

# for (symbol,) in symbolList:
#     for url in urls:
#     t = Thread(target=requestThread, args=(url,))
#     t.start()
#     threadList.append(t)
#     for b in threadList:
#             b.join()
#
#     # htmlText = urllib.urlopen("http://www.bloomberg.com/markets/chart/data/1D/" + symbol + ":US")
#     data = json.load(htmlText)
#     datapoint = data["data_values"]
#     for point in datapoints:
#       print "symbol", symbol, "time", point[0], "price", point[1]
#
#     myFile = open("stock_price/daily_prices/" + symbol + ".txt", "a"
#     for point in datapoints:
#       myFile.write(str(symbol + "," + str(point[0] + "," + str(point[1] + "\n")))
#     myFile.close()
#
#     data = ystockquote.get_historical_prices(symbol, start_date, end_date)
#     for (date, dailyData) in data.items():
#         print(date)
#         for (key, value) in dailyData.items():
#             print(symbol + " " + key + " " + value)
# cur.close()
# db.close()