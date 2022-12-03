# import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
from api_token import IEX_CLOUD_API_TOKEN
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# read top 500 stocks to pandas data frame
stocks = pd.read_csv('sp_500_stocks.csv')
stocks = stocks[~stocks['Ticker'].isin(['DISCA', 'HFC','VIAC','WLTW'])]

# getting market cap and stock price for each stock
symbol = "AAPL"
stock_price_api_endpoint = f"https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}"
data = requests.get(stock_price_api_endpoint).json()  # returns json object of symbol
price = data["latestPrice"]
market_cap = data["marketCap"]


# split list of tickers into sub-lists to make batch API calls
def split_list(lst, n):
    for x in range(0, len(lst), n):
        yield lst[x:x+n]


symbols_groups = list(split_list(stocks['Ticker'], 100))  # store 5 lists of 100 stocks
symbol_strings = []
# append a string of each a hundred stocks in symbol strings
for i in range(0, len(symbols_groups)):
    symbol_strings.append(','.join(symbols_groups[i]))

# adding first set of data to pandas data frame
columns = ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy']
dataframe = pd.DataFrame(columns=columns)  # empty dataframe that can be used to append rows
new_row = pd.DataFrame([symbol, price, market_cap, "N/A"], index=columns).T
new_dataframe = pd.concat((dataframe, new_row))  # dataframe after row has been appended

# loop through each symbol_string and make batch API call for each symbol
for symbol_string in symbol_strings:
    batch_api_call = f"https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}"
    data = requests.get(batch_api_call).json()  # returns json object of symbol_strings
    # get each symbol_string in symbol_strings and append information to dataframe
    for symbol in symbol_string.split(','):
        new_row = pd.DataFrame([symbol,
                                data[symbol]['quote']['latestPrice'],
                                data[symbol]['quote']['marketCap'], "N/A"],
                               index=columns).T
        new_dataframe = pd.concat((new_dataframe, new_row))

