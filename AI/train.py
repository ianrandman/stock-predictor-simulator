from keras import optimizers
from sklearn.preprocessing import MinMaxScaler
import random
import numpy as np
import os
import shutil
import requests
from io import open
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense, CuDNNLSTM
from keras.layers import LSTM
from keras.layers import Dropout

DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'
MINUTES_IN_DAY = 1440
NUM_DAYS_TO_TRAIN = 9


def load_candles():
    candle_data_path = DATA_PATH + 'crypto_candles-more/'
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

    crypto_candles_list_scaled = scale(crypto_candles_list)

    for i in range(len(crypto_candles_list)):
        crypto_candles = crypto_candles_list_scaled[i]
        for j in range(int(NUM_DAYS_TO_TRAIN * MINUTES_IN_DAY / resolution), crypto_candles.shape[0]):
            features_set.append(crypto_candles[j - int(NUM_DAYS_TO_TRAIN * MINUTES_IN_DAY / resolution):j])

            # Calculate % change for target
            start = crypto_candles_list[i].iloc[int(j - MINUTES_IN_DAY / resolution), 0]  # close of day before
            end = crypto_candles_list[i].iloc[j, 0]  # close of day

            percent_change = 100 * (end - start) / start
            targets.append(percent_change)

    features_set, targets = np.array(features_set), np.array(targets)

    return features_set, targets


def train(features_set, targets):
    features_set = features_set[:17312]
    targets = targets[:17312]

    model = Sequential()

    model.add(
        LSTM(100, batch_input_shape=(32, 9, features_set.shape[2]),
             stateful=True, kernel_initializer='random_uniform'))
    model.add(Dropout(0.5))
    model.add(Dense(20, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    optimizer = optimizers.RMSprop(lr=0.001)
    model.compile(loss='mean_squared_error', optimizer=optimizer)

    # model.add(LSTM(units=50, return_sequences=True, input_shape=(features_set.shape[1], features_set.shape[2])))
    # model.add(Dropout(0.2))
    #
    # model.add(LSTM(units=50, return_sequences=True))
    # model.add(Dropout(0.2))
    #
    # model.add(LSTM(units=50, return_sequences=True))
    # model.add(Dropout(0.2))
    #
    # model.add(LSTM(units=50))
    # model.add(Dropout(0.2))
    #
    # model.add(Dense(units=1))
    #
    # model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(features_set, targets, epochs=100, batch_size=32)


def main():
    crypto_candles_list = load_candles()
    features_set, targets = build_candle_features_and_targets(crypto_candles_list)
    train(features_set, targets)


if __name__ == '__main__':
    main()