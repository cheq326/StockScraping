import mysql.connector
import sys
import urllib.request
import re
import ystockquote
import datetime

db = mysql.connector.connect(host="localhost", # your host, usually localhost
                     user="chenq", # your username
                      passwd="admin", # your password
                      db="stock") # name of the data base

cur = db.cursor()
cur.execute("select symbol from stock_symbol")
rows = cur.fetchall()

base_url = "http://ichart.finance.yahoo.com/table.csv?s="
def make_url(ticker_symbol):
    return base_url + ticker_symbol

output_path = "D:"
def make_filename(ticker_symbol, directory="S&P"):
    return output_path + "/" + directory + "/" + ticker_symbol + ".csv"

def pull_historical_data(ticker_symbol, directory="S&P"):
    try:
        urllib.request.urlretrieve(make_url(ticker_symbol), make_filename(ticker_symbol, directory))
    except urllib.request.ContentTooShortError as e:
        outfile = open(make_filename(ticker_symbol, directory), "w")
        outfile.write(e.content)
        outfile.close()

for (symbol,) in rows:
    pull_historical_data(symbol)