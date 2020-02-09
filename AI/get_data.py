"""
This should be used to retrieve Reddit posts using Reddit's Praw. Then split the data.
usage: get_data.py
__author__ = Ian Randman
__author__ = David Dunlap
"""

import random
import threading
import numpy as np
import os
import shutil
import requests
from io import open

import pandas as pd

with open('./api_key.txt', 'r') as f:
    api_key = f.readline()


subreddit_names = ['nba', 'nhl', 'nfl', 'mlb', 'soccer', 'formula1', 'CFB', 'sports']
sub_to_num = {'r/nba': 0, 'r/nhl': 1, 'r/nfl': 2, 'r/mlb': 3, 'r/soccer': 4, 'r/formula1': 5, 'r/CFB': 6, 'r/sports': 7}
num_to_sub = {0: 'r/nba', 1: 'r/nhl', 2: 'r/nfl', 3: 'r/mlb', 4: 'r/soccer', 5: 'r/formula1', 6: 'r/CFB', 7: 'r/sports'}

DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'


def get_symbols():
    data_file_path = DATA_PATH + 'symbols.csv'
    if os.path.isfile(data_file_path):
        df = pd.read_csv(data_file_path, index_col=0)
    else:
        df = pd.DataFrame()
        markets = list()
        symbols = list()

        request_parameters = dict()
        request_parameters['format'] = 'csv'
        request_parameters['exchange'] = 'binance'
        request_parameters['token'] = api_key

        base_url = 'https://finnhub.io/api/v1/crypto/symbol'
        r = requests.get(base_url, params=request_parameters)

        for crypto in r.json():
            market = crypto['description'].split()[1]
            if 'USDT' == market[-4:]:
                markets.append(market)
                symbols.append(crypto['symbol'])

        df['markets'] = markets
        df['symbols'] = symbols
        df.to_csv(data_file_path)

    return df


def get_candles(symbols):
    candle_data_path = DATA_PATH + 'crypto_candles/'
    crypto_candles = list()

    if os.path.exists(candle_data_path):
        pass
        # for file_name in os.listdir(candle_data_path):
        #     df = pd.read_csv(candle_data_path + file_name, index_col=0)
        #     crypto_candles.append(df)
    else:
        os.makedirs(candle_data_path)

        base_url = 'https://finnhub.io/api/v1/crypto/candle'

        request_parameters = dict()
        # request_parameters['format'] = 'csv'
        request_parameters['resolution'] = 'D'
        request_parameters['from'] = '1549584000'  # 02/08/2019 @ 12:00am (UTC)
        request_parameters['to'] = '1581120000'  # 02/08/2020 @ 12:00am (UTC)
        request_parameters['token'] = api_key

        for index, row in symbols.iterrows():
            market = row['markets']
            symbol = row['symbols']

            request_parameters['symbol'] = symbol
            r = requests.get(base_url, params=request_parameters)

            try:
                if r.json()['s'] == 'no_data':
                    continue

            except ValueError:
                continue

            candles = pd.DataFrame.from_dict(r.json())
            candles.drop('s', axis=1, inplace=True)
            candles.to_csv(candle_data_path + market + '.csv')
            crypto_candles.append(candles)


def main():
    symbols = get_symbols()
    get_candles(symbols)


if __name__ == '__main__':
    main()

    # if os.path.exists(DATA_PATH):
    #     shutil.rmtree(DATA_PATH)
    #
    # os.makedirs(DATA_PATH)
    #
    # threads = list()
    # limit = 1000
    # print('Downloading', limit, 'posts from each subreddit\n')
    #
    # for subreddit_name in subreddit_names:
    #     thread = threading.Thread(target=save_posts, args=(subreddit_name, limit,))
    #     thread.start()
    #     threads.append(thread)
    #
    # for thread in threads:
    #     thread.join()
    #
    # split_data()
    #
    # print('\nDownload finished')




















def what():
    base_url = 'https://finnhub.io/api/v1/crypto/candle'

    request_parameters = dict()
    request_parameters['format'] = 'csv'
    request_parameters['resolution'] = 'D'
    request_parameters['from'] = '1549584000'  # 02/08/2019 @ 12:00am (UTC)
    request_parameters['to'] = '1581120000'  # 02/08/2020 @ 12:00am (UTC)
    request_parameters['symbol'] = 'BINANCE:BTCUSDT'
    request_parameters['token'] = api_key

    r = requests.get(base_url, params=request_parameters)

    # r = requests.get('https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&format=csv&resolution=D&from=1549584000&to=1581120000&token=' + api_key)

    # r = requests.get('https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=D&resolution=D&from=1549584000&to=Unix.Now&token=' + api_key)
    print(r.text)
