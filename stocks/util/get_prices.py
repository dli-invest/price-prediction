import yfinance as yf
import pandas as pd 
import yaml
import os
def get_prices(stocks, start_date="2020-03-01", end_date="2020-05-30"):
    stocks_string = " ".join(stocks)
    data = yf.download(stocks_string, start=start_date, end=end_date,
                      group_by="ticker")
    data = data.fillna(method='ffill')
    # Drop columns with no entries
    data = data.dropna(axis='columns', how='all')

    prices_df = pd.concat([data[ticker]["Close"] for ticker in stocks], axis=1)
    prices_df.columns = stocks
    return prices_df

# Rename this later
def get_config(upload_file = 'config.yml'):
    exists = os.path.isfile('stocks/config.yml')
    if exists:
        config_file = 'stocks/config.yml'
        # Store configuration file values
    else:
        # Keep presets
        config_file = upload_file
    with open(config_file, 'r') as ymlfile:
        # Latest version
        if hasattr(yaml, 'FullLoader'):
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        # PyYaml 3.
        else:
            cfg = yaml.load(ymlfile)
    return cfg
