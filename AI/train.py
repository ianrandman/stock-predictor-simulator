from sklearn.preprocessing import MinMaxScaler
import random
import numpy as np
import os
import shutil
import requests
from io import open
import pandas as pd

DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'
MINUTES_IN_DAY = 1440
NUM_DAYS_TO_TRAIN = 9


def load_candles():
    candle_data_path = DATA_PATH + 'crypto_candles/'
    crypto_candles_list = list()

    if os.path.exists(candle_data_path):
        for file_name in os.listdir(candle_data_path):
            df = pd.read_csv(candle_data_path + file_name, index_col=0)
            crypto_candles_list.append(df)

    return crypto_candles_list


def scale(crypto_candles_list):
    scaler = MinMaxScaler(feature_range=(0, 1))

    crypto_candles_list_scaled = list()
    for crypto_candles in crypto_candles_list:
        crypto_candles.drop('t', axis=1, inplace=True)
        crypto_candles_scaled = scaler.fit_transform(crypto_candles)  # TODO all cryptos
        crypto_candles_list_scaled.append(crypto_candles_scaled)

    return crypto_candles_list_scaled


def build_candle_features_and_targets(crypto_candles_list, resolution=MINUTES_IN_DAY):
    features_set = list()
    targets = list()

    for crypto_candles in crypto_candles_list[0:1]:
        for i in range(int(NUM_DAYS_TO_TRAIN * MINUTES_IN_DAY / resolution), crypto_candles.shape[0]):
            features_set.append(crypto_candles[i - int(NUM_DAYS_TO_TRAIN * MINUTES_IN_DAY / resolution):i])

            # Calculate % change for target
            start = crypto_candles[int(i - MINUTES_IN_DAY / resolution)][0]  # close of day before
            end = crypto_candles[i][0]  # close of day

            percent_change = (end - start) / start
            targets.append(percent_change)

    features_set, targets = np.array(features_set), np.array(targets)

    return features_set, targets


def main():
    crypto_candles_list = load_candles()
    crypto_candles_list_scaled = scale(crypto_candles_list)
    build_candle_features_and_targets(crypto_candles_list_scaled)


if __name__ == '__main__':
    main()