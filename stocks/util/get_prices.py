import yfinance as yf
import pandas as pd 

def get_prices(stocks, start_date="2020-03-01", end_date="2020-05-30"):
    stocks_string = " ".join(stocks)
    data = yf.download(stocks_string, start=start_date, end=end_date,
                      group_by="ticker")
    data = data.fillna(method='ffill')
    # Drop columns with no entries
    data = data.dropna(axis='columns', how='all')

    prices_df = pd.concat([data[ticker]["Close"] for ticker in stocks], axis=1)
    return prices_df