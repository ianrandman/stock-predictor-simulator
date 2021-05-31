import sys

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta

TRAIN = False


def download_training_data():
    granularities = [60, 300, 900, 3600, 21600]  # in seconds
    products = ['BTC', 'ETH']

    days_to_go_back = 365 * 4

    for product in products:
        base_url = f'https://api.pro.coinbase.com/products/{product}-USD/candles'
        for granularity in granularities:

            delta = timedelta(seconds=granularity)
            current_time = datetime.now()
            start_time = current_time - timedelta(days=days_to_go_back)

            df = pd.DataFrame(columns=['time', 'low', 'high', 'open', 'close', 'volume'])
            while start_time < current_time:
                end_time = start_time + delta * 250  # max of 300

                payload = {
                    'start': start_time,
                    'end': end_time,
                    'granularity': granularity
                }

                response = requests.get(base_url, params=payload)
                if not response.status_code == 200:
                    print('ERROR RETRIEVING DATA')
                    sys.exit(1)

                df = df.append(pd.DataFrame(reversed(response.json()), columns=df.columns))

                start_time = end_time
                # print(end_time)

            df.to_csv(f'data/{product}_{granularity}.csv', index=False)
            print(f'data/{product}_{granularity}.csv')


def download_new_data():
    granularity = 60 * 60  # in seconds
    product = 'BTC'

    days_to_go_back = 4

    base_url = f'https://api.pro.coinbase.com/products/{product}-USD/candles'

    delta = timedelta(seconds=granularity)
    current_time = datetime.now()
    start_time = current_time - timedelta(days=days_to_go_back)

    df = pd.DataFrame(columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    while start_time < current_time:
        end_time = start_time + delta * 250  # max of 300

        payload = {
            'start': start_time,
            'end': end_time,
            'granularity': granularity
        }

        response = requests.get(base_url, params=payload)
        if not response.status_code == 200:
            print('ERROR RETRIEVING DATA')
            sys.exit(1)

        df = df.append(pd.DataFrame(reversed(response.json()), columns=df.columns))

        start_time = end_time
        # print(end_time)

    df.to_csv(f'data/new_{product}_{granularity}.csv', index=False)
    print(f'data/new_{product}_{granularity}.csv')


if __name__ == '__main__':
    if TRAIN:
        download_new_data()
    else:
        download_new_data()