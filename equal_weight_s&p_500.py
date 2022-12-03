import pandas as pd
import requests
import math
from api_token import IEX_CLOUD_API_TOKEN
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    # read top 500 stocks to pandas data frame
    stocks = pd.read_csv('sp_500_stocks.csv')
    stocks = stocks[~stocks['Ticker'].isin(['DISCA', 'HFC','VIAC','WLTW'])]

    # getting market cap and stock price for first stock
    symbol = "A"
    stock_price_api_endpoint = f"https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}"
    data = requests.get(stock_price_api_endpoint).json()  # returns json object of symbol
    price = data["latestPrice"]
    market_cap = data["marketCap"]

    # store 5 lists of 100 stocks
    symbols_groups = list(split_list(stocks['Ticker'], 100))
    symbol_strings = []

    # append a string of each a hundred stocks into symbol strings
    for i in range(0, len(symbols_groups)):
        symbol_strings.append(','.join(symbols_groups[i]))

    # adding first set of data to pandas data frame
    columns = ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy']
    starter_dataframe = pd.DataFrame(columns=columns)  # empty dataframe that can be used to append rows
    new_row = pd.DataFrame([symbol, price, market_cap, "N/A"], index=columns).T
    final_dataframe = pd.concat((starter_dataframe, new_row))  # dataframe after row has been appended

    # loop through remaining symbol_strings and make batch API call for each symbol
    for symbol_string in symbol_strings:
        batch_api_call = f"https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}"
        data = requests.get(batch_api_call).json()  # returns json object of symbol_strings
        # get each symbol_string in symbol_strings and append information to dataframe
        for symbol in symbol_string.split(',')[1:]:  # start at index one since 'A' has already been added
            new_row = pd.DataFrame([symbol,  # create row with new data
                                    data[symbol]['quote']['latestPrice'],
                                    data[symbol]['quote']['marketCap'], "N/A"],
                                   index=columns).T
            # concatenate new row of data to dataframe
            final_dataframe = pd.concat((final_dataframe, new_row), ignore_index=True)

    # calculate number of shares to user should buy
    while True:
        try:
            portfolio_amount = float(input("Enter the value of your portfolio: "))
            if type(portfolio_amount) == float:
                break
        except ValueError:
            print("\nPortfolio amount must be a decimal.")

    position_size = portfolio_amount / len(final_dataframe.index)
    for i in range(0, len(final_dataframe.index)):
        final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Stock Price'])

    # format output
    format_excel_output(final_dataframe)
    print("Output has been placed in: 'recommended trades.xlsx'")


def split_list(lst, n):
    """Returns a sublist of a list of n size"""
    for x in range(0, len(lst), n):
        yield lst[x:x+n]


def format_excel_output(dataframe):
    """saves and formats dataframe into an Excel file"""
    writer = pd.ExcelWriter('recommended trades.xlsx', engine='xlsxwriter')
    dataframe.to_excel(writer, 'Recommended Trades', index=False)

    background_color = '#ffffff'
    font_color = '#000000'

    string_format = writer.book.add_format(  # format for strings
        {
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    dollar_format = writer.book.add_format(  # format for currency
        {
            'num_format': '$0.00',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    integer_format = writer.book.add_format(  # format for integers
        {
            'num_format': '0',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    columns_formats = {  # format for column names
        'A': ['Ticker', string_format],
        'B': ['Stock Price', dollar_format],
        'C': ['Market Capitalization', dollar_format],
        'D': ['Number of Shares to Buy', integer_format]
    }

    for column in columns_formats.keys():
        writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 18, columns_formats[column][1])
        writer.sheets['Recommended Trades'].write(f'{column}1', columns_formats[column][0], columns_formats[column][1])
    writer.save()


if __name__ == "__main__":
    main()
