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
    candle_data_path = DATA_PATH + 'crypto_data_new_api/'
    crypto_data_list = list()

    if os.path.exists(candle_data_path):
        for file_name in os.listdir(candle_data_path):
            df = pd.read_csv(candle_data_path + file_name, index_col=0)
            crypto_data_list.append(df)

    return crypto_data_list


def scale(crypto_data_list):
    scaler = MinMaxScaler(feature_range=(0, 10))

    crypto_data_list_scaled = list()
    for crypto_data in crypto_data_list:
        crypto_data.drop('dates', axis=1, inplace=True)
        crypto_data_scaled = scaler.fit_transform(crypto_data)  # TODO all cryptos
        crypto_data_list_scaled.append(crypto_data_scaled)

    return crypto_data_list_scaled


def build_candle_features_and_targets(crypto_data_list, resolution=MINUTES_IN_DAY):
    features_set = list()
    targets = list()

    crypto_data_list_scaled = scale(crypto_data_list)

    for i in range(len(crypto_data_list)):
        crypto_data = crypto_data_list_scaled[i]
        for j in range(int(NUM_DAYS_TO_TRAIN * MINUTES_IN_DAY / resolution), crypto_data.shape[0]):
            features_set.append(crypto_data[j - int(NUM_DAYS_TO_TRAIN * MINUTES_IN_DAY / resolution):j])

            # Calculate % change for target
            # start = crypto_data_list[i].iloc[int(j - MINUTES_IN_DAY / resolution), 0]  # close of day before
            # end = crypto_data_list[i].iloc[j, 0]  # close of day
            #
            # percent_change = 100 * (end - start) / start

            change = crypto_data_list[i].iloc[j, 0] - crypto_data_list[i].iloc[int(j - MINUTES_IN_DAY / resolution), 0]
            if change <= 0:
                targets.append(0)
            else:
                targets.append(1)

            # targets.append(percent_change)

    features_set, targets = np.array(features_set), np.array(targets)

    return features_set, targets


def train(features_set, targets):
    features_set_train = features_set[:1280]
    targets_train = targets[:1280]

    model = Sequential()

    model.add(
        LSTM(75, batch_input_shape=(16, NUM_DAYS_TO_TRAIN, features_set_train.shape[2]),
             stateful=True, kernel_initializer='random_uniform', return_sequences=False))
    model.add(Dropout(0.2))

    # model.add(
    #     LSTM(25, batch_input_shape=(16, NUM_DAYS_TO_TRAIN, features_set.shape[2]),
    #          stateful=True, kernel_initializer='random_uniform'))
    # model.add(Dropout(0.5))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    optimizer = optimizers.Adam(lr=0.001)
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

    model.fit(features_set_train, targets_train, epochs=100, batch_size=16)

    print(model.evaluate(features_set[1280:1728], targets[1280:1728], batch_size=16))


def main():
    crypto_data_list = load_candles()
    features_set, targets = build_candle_features_and_targets(crypto_data_list)
    train(features_set, targets)


if __name__ == '__main__':
    main()