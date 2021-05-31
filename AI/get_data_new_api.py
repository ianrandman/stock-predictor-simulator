"""
This should be used to retrieve Reddit posts using Reddit's Praw. Then split the data.
usage: get_data.py
__author__ = Ian Randman
__author__ = David Dunlap
"""

import random
import threading
from time import sleep

import numpy as np
import os
import shutil
import requests
from io import open
import pandas as pd

with open('./new_api_key.txt', 'r') as f:
    api_key = f.readline()

DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'


def get_symbols():
    return ['ETH', 'BCH', 'LTC']  # TODO add more


def get_candles(symbols):
    crypto_data_path = DATA_PATH + 'crypto_data_new_api/'
    crypto_data = list()

    if os.path.exists(crypto_data_path):
        pass
        # for file_name in os.listdir(candle_data_path):
        #     df = pd.read_csv(candle_data_path + file_name, index_col=0)
        #     crypto_candles.append(df)
    else:
        os.makedirs(crypto_data_path)

        base_url = 'https://www.alphavantage.co/query'

        request_parameters = dict()
        # request_parameters['format'] = 'csv'
        # request_parameters['from'] = '1420070400'  # 01/01/2015 @ 12:00am (UTC)
        # request_parameters['to'] = '1581221249856'  # 02/08/2020 @ 12:00am (UTC)
        request_parameters['apikey'] = api_key

        for symbol in symbols:
            request_parameters['symbol'] = symbol

            # OHCLV
            request_parameters['function'] = 'DIGITAL_CURRENCY_DAILY'
            request_parameters['market'] = 'USD'

            r = requests.get(base_url, params=request_parameters)
            while r.status_code != 200 or 'Note' in r.json().keys():
                print('Waiting (API limit may be reached)...')
                sleep(5)
                r = requests.get(base_url, params=request_parameters)

            dates = list()
            opens = list()
            highs = list()
            lows = list()
            closes = list()
            volumes = list()
            market_caps = list()
            for date in r.json()['Time Series (Digital Currency Daily)']:
                dates.append(date)
                date_data = r.json()['Time Series (Digital Currency Daily)'][date]

                opens.append(date_data['1a. open (USD)'])
                highs.append(date_data['2a. high (USD)'])
                lows.append(date_data['3a. low (USD)'])
                closes.append(date_data['4a. close (USD)'])
                volumes.append(date_data['5. volume'])
                market_caps.append(date_data['6. market cap (USD)'])

            # Indicators
            request_parameters['function'] = 'SMA'
            request_parameters['interval'] = 'daily'
            request_parameters['time_period'] = '10'
            request_parameters['series_type'] = 'open'
            del request_parameters['market']

            r = requests.get(base_url, params=request_parameters)
            while r.status_code != 200 or 'Note' in r.json().keys():
                print('Waiting (API limit may be reached)...')
                sleep(5)
                r = requests.get(base_url, params=request_parameters)

            smas_10 = list()
            for i in range(len(dates)):
                date = dates[i]

                if date in r.json()['Technical Analysis: SMA']:
                    smas_10.append(float(r.json()['Technical Analysis: SMA'][date]['SMA']))
                else:
                    smas_10.append(0.0)


            request_parameters['time_period'] = '20'
            r = requests.get(base_url, params=request_parameters)
            while r.status_code != 200 or 'Note' in r.json().keys():
                print('Waiting (API limit may be reached)...')
                sleep(5)
                r = requests.get(base_url, params=request_parameters)

            smas_20 = list()
            for i in range(len(dates)):
                date = dates[i]

                if date in r.json()['Technical Analysis: SMA']:
                    smas_20.append(float(r.json()['Technical Analysis: SMA'][date]['SMA']))
                else:
                    smas_20.append(0.0)

            request_parameters['time_period'] = '30'
            r = requests.get(base_url, params=request_parameters)
            while r.status_code != 200 or 'Note' in r.json().keys():
                print('Waiting (API limit may be reached)...')
                sleep(5)
                r = requests.get(base_url, params=request_parameters)

            smas_30 = list()
            for i in range(len(dates)):
                date = dates[i]

                if date in r.json()['Technical Analysis: SMA']:
                    smas_30.append(float(r.json()['Technical Analysis: SMA'][date]['SMA']))
                else:
                    smas_30.append(0.0)

            data = dict()
            data['dates'] = dates
            data['opens'] = opens
            data['highs'] = highs
            data['lows'] = lows
            data['closes'] = closes
            data['volumes'] = volumes
            data['market_caps'] = market_caps
            data['smas_10'] = smas_10
            data['smas_20'] = smas_20
            data['smas_30'] = smas_30

            ##############

            df = pd.DataFrame.from_dict(data)
            df.to_csv(crypto_data_path + symbol + '.csv')

            crypto_data.append(df)


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
    request_parameters['resolution'] = '60'
    request_parameters['from'] = '1549584000'  # 02/08/2019 @ 12:00am (UTC)
    request_parameters['to'] = '1581120000'  # 02/08/2020 @ 12:00am (UTC)
    request_parameters['symbol'] = 'BINANCE:BTCUSDT'
    request_parameters['token'] = api_key

    r = requests.get(base_url, params=request_parameters)

    # r = requests.get('https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&format=csv&resolution=D&from=1549584000&to=1581120000&token=' + api_key)

    # r = requests.get('https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=D&resolution=D&from=1549584000&to=Unix.Now&token=' + api_key)
    print(r.text)
