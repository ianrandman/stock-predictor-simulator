import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from tqdm.contrib import tzip
from yahoo_fin import stock_info as si
from collections import deque

import numpy as np
import pandas as pd
import random

# set seed, so we can get the same results after rerunning several times
from AI_v2.process import load_data

np.random.seed(314)
tf.random.set_random_seed(314)
# tf.random.set_seed(314)
random.seed(314)


def shuffle_in_unison(a, b):
    # shuffle two arrays in the same way
    state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(state)
    np.random.shuffle(b)


def preprocess_data(ticker, n_steps=50, scale=True, shuffle=True, lookup_step=1, split_by_date=False,
                    test_size=0.001, feature_columns=['low', 'high', 'open', 'volume', 'hour', 'minute']):
    """
    Loads data from Yahoo Finance source, as well as scaling, shuffling, normalizing and splitting.
    Params:
        ticker (str/pd.DataFrame): the ticker you want to load, examples include AAPL, TESL, etc.
        n_steps (int): the historical sequence length (i.e window size) used to predict, default is 50
        scale (bool): whether to scale prices from 0 to 1, default is True
        shuffle (bool): whether to shuffle the dataset (both training & testing), default is True
        lookup_step (int): the future lookup step to predict, default is 1 (e.g next day)
        split_by_date (bool): whether we split the dataset into training/testing by date, setting it
            to False will split datasets in a random way
        test_size (float): ratio for test data, default is 0.2 (20% testing data)
        feature_columns (list): the list of features to use to feed into the model, default is everything grabbed from yahoo_fin
    """
    # # see if ticker is already a loaded stock from yahoo finance
    # if isinstance(ticker, str):
    #     # load it from yahoo_fin library
    #     df = si.get_data(ticker)
    # elif isinstance(ticker, pd.DataFrame):
    #     # already loaded, use it directly
    #     df = ticker
    # else:
    #     raise TypeError("ticker can be either a str or a `pd.DataFrame` instances")

    total_df, dfs = load_data()
    # df = dfs[0]

    # this will contain all the elements we want to return from this function
    result = dict()
    # we will also return the original dataframe itself
    result['total_df'] = total_df.copy()
    result['dfs'] = [df.copy() for df in dfs]

    # # make sure that the passed feature_columns exist in the dataframe
    # for col in feature_columns:
    #     assert col in df.columns, f"'{col}' does not exist in the dataframe."
    #
    # # add date as a column
    # if "date" not in df.columns:
    #     df["date"] = df.index

    # if scale:
    total_df['low'] = np.log(total_df['low'])
    total_df['high'] = np.log(total_df['high'])
    total_df['open'] = np.log(total_df['open'])
    total_df['close'] = np.log(total_df['close'])
    total_df['volume'] = np.log(total_df['volume'])

    column_scaler = {}
    # scale the data (prices) from 0 to 1
    for column in feature_columns + ['close']:
        scaler = preprocessing.MinMaxScaler()
        total_df[column] = scaler.fit_transform(np.expand_dims(total_df[column].values, axis=1))
        column_scaler[column] = scaler

    # add the MinMaxScaler instances to the result returned
    result["column_scaler"] = column_scaler

    all_sequence_data = list()
    print('Creating sequences...')
    with tqdm(total=len(total_df)) as t:
        for df in dfs:
            df['low'] = np.log(df['low'])
            df['high'] = np.log(df['high'])
            df['open'] = np.log(df['open'])
            df['close'] = np.log(df['close'])
            df['volume'] = np.log(df['volume'])

            for column in feature_columns + ['close']:
                scaler = column_scaler[column]
                df[column] = scaler.transform(np.expand_dims(df[column].values, axis=1))

            # add the target column (label) by shifting by `lookup_step`
            df['future'] = df['close'].shift(-lookup_step)
            del df['close']

        # # last `lookup_step` columns contains NaN in future column
        # # get them before dropping NaNs
        # last_sequence = np.array(df[feature_columns].tail(lookup_step))

            # drop NaNs
            df.dropna(inplace=True)

            sequence_data = list()
            sequences = deque(maxlen=n_steps)

            for entry, target in zip(df[feature_columns + ['time']].values, df['future'].values):
                sequences.append(entry)
                if len(sequences) == n_steps:
                    sequence_data.append([np.array(sequences), target])
                t.update()

            all_sequence_data.extend(sequence_data)

    # # get the last sequence by appending the last `n_step` sequence with `lookup_step` sequence
    # # for instance, if n_steps=50 and lookup_step=10, last_sequence should be of 60 (that is 50+10) length
    # # this last_sequence will be used to predict future stock prices that are not available in the dataset
    # last_sequence = list([s[:len(feature_columns)] for s in sequences]) + list(last_sequence)
    # last_sequence = np.array(last_sequence).astype(np.float32)
    # # add to result
    # result['last_sequence'] = last_sequence

    # construct the X's and y's
    X, y = list(), list()
    print('Appending...')
    for seq, target in tqdm(all_sequence_data):
        X.append(seq)
        y.append(target)

    # convert to numpy arrays
    X = np.array(X)
    y = np.array(y)

    if split_by_date:
        # split the dataset into training & testing sets by date (not randomly splitting)
        train_samples = int((1 - test_size) * len(X))
        result["X_train"] = X[:train_samples]
        result["y_train"] = y[:train_samples]
        result["X_test"] = X[train_samples:]
        result["y_test"] = y[train_samples:]
        if shuffle:
            # shuffle the datasets for training (if shuffle parameter is set)
            shuffle_in_unison(result["X_train"], result["y_train"])
            shuffle_in_unison(result["X_test"], result["y_test"])
    else:
        # split the dataset randomly
        result["X_train"], result["X_test"], result["y_train"], result["y_test"] = train_test_split(X, y,
                                                                                                    test_size=test_size,
                                                                                                    shuffle=shuffle)

    # # get the list of test set dates
    dates = result["X_test"][:, -1, -1]
    result['dates'] = result['X_test'][:, :, -1]
    # [result['total_df'][result['total_df']['time'].isin(dates)] for dates in result['X_test'][:, :, -1]]
    # # retrieve test features from the original dataframe
    # result["test_df"] = result["df"].loc[dates]
    print('Creating test df...')
    result["test_df"] = result["total_df"][result["total_df"]['time'].isin(dates)]
    # # remove duplicated dates in the testing dataframe
    # result["test_df"] = result["test_df"][~result["test_df"].index.duplicated(keep='first')]
    # remove dates from the training/testing sets & convert to float32
    result["X_train"] = result["X_train"][:, :, :len(feature_columns)].astype(np.float32)
    result["X_test"] = result["X_test"][:, :, :len(feature_columns)].astype(np.float32)

    return result


def preprocess_data_test(ticker, column_scaler, n_steps=50, lookup_step=1, feature_columns=['low', 'high', 'open', 'volume', 'hour', 'minute']):
    total_df, dfs = load_data(train=False)
    # df = dfs[0]

    # this will contain all the elements we want to return from this function
    result = dict()
    result["column_scaler"] = column_scaler

    # we will also return the original dataframe itself
    result['total_df'] = total_df.copy()
    # result['dfs'] = [df.copy() for df in dfs]
    #
    # # # make sure that the passed feature_columns exist in the dataframe
    # # for col in feature_columns:
    # #     assert col in df.columns, f"'{col}' does not exist in the dataframe."
    # #
    # # # add date as a column
    # # if "date" not in df.columns:
    # #     df["date"] = df.index

    # # if scale:
    # total_df['low'] = np.log(total_df['low'])
    # total_df['high'] = np.log(total_df['high'])
    # total_df['open'] = np.log(total_df['open'])
    # total_df['close'] = np.log(total_df['close'])
    # total_df['volume'] = np.log(total_df['volume'])
    #
    # column_scaler = {}
    # # scale the data (prices) from 0 to 1
    # for column in feature_columns + ['close']:
    #     scaler = column_scaler[column]
    #     total_df[column] = scaler.fit_transform(np.expand_dims(total_df[column].values, axis=1))
    #
    # # add the MinMaxScaler instances to the result returned
    # result["column_scaler"] = column_scaler

    # all_sequence_data = list()
    print('Creating sequences...')
    # with tqdm(total=len(total_df)) as t:
    #     for df in dfs:
    total_df['low'] = np.log(total_df['low'])
    total_df['high'] = np.log(total_df['high'])
    total_df['open'] = np.log(total_df['open'])
    total_df['close'] = np.log(total_df['close'])
    total_df['volume'] = np.log(total_df['volume'])

    for column in feature_columns + ['close']:
        scaler = column_scaler[column]
        total_df[column] = scaler.transform(np.expand_dims(total_df[column].values, axis=1))

    # add the target column (label) by shifting by `lookup_step`
    total_df['future'] = total_df['close'].shift(-lookup_step)
    del total_df['close']

# # last `lookup_step` columns contains NaN in future column
# # get them before dropping NaNs
# last_sequence = np.array(total_df[feature_columns].tail(lookup_step))

    # drop NaNs
    total_df.dropna(inplace=True)

    sequence_data = list()
    sequences = deque(maxlen=n_steps)

    for entry, target in tzip(total_df[feature_columns + ['time']].values, total_df['future'].values):
        sequences.append(entry)
        if len(sequences) == n_steps:
            sequence_data.append([np.array(sequences), target])

    # all_sequence_data.extend(sequence_data)

    # # get the last sequence by appending the last `n_step` sequence with `lookup_step` sequence
    # # for instance, if n_steps=50 and lookup_step=10, last_sequence should be of 60 (that is 50+10) length
    # # this last_sequence will be used to predict future stock prices that are not available in the dataset
    # last_sequence = list([s[:len(feature_columns)] for s in sequences]) + list(last_sequence)
    # last_sequence = np.array(last_sequence).astype(np.float32)
    # # add to result
    # result['last_sequence'] = last_sequence

    # construct the X's and y's
    X, y = list(), list()
    print('Appending...')
    for seq, target in tqdm(sequence_data):
        X.append(seq)
        y.append(target)

    # convert to numpy arrays
    X = np.array(X)
    y = np.array(y)

    result['X'] = X
    result['y'] = y
    # if split_by_date:
    #     # split the dataset into training & testing sets by date (not randomly splitting)
    #     train_samples = int((1 - test_size) * len(X))
    #     result["X_train"] = X[:train_samples]
    #     result["y_train"] = y[:train_samples]
    #     result["X_test"] = X[train_samples:]
    #     result["y_test"] = y[train_samples:]
    #     if shuffle:
    #         # shuffle the datasets for training (if shuffle parameter is set)
    #         shuffle_in_unison(result["X_train"], result["y_train"])
    #         shuffle_in_unison(result["X_test"], result["y_test"])
    # else:
    #     # split the dataset randomly
    # #     result["X_train"], result["X_test"], result["y_train"], result["y_test"] = train_test_split(X, y,
    #                                                                                                 test_size=test_size,
    #                                                                                     shuffle=shuffle)

    # # # get the list of test set dates
    # dates = result["X_test"][:, -1, -1]
    # result['dates'] = result['X_test'][:, :, -1]
    # # [result['total_df'][result['total_df']['time'].isin(dates)] for dates in result['X_test'][:, :, -1]]
    # # # retrieve test features from the original dataframe
    # # result["test_df"] = result["df"].loc[dates]
    print('Creating test df...')
    dates = result["X"][:, -1, -1]
    result["test_df"] = result["total_df"][result["total_df"]['time'].isin(dates)]
    # result["test_df"] = result["total_df"][result["total_df"]['time'].isin(dates)]
    # # # remove duplicated dates in the testing dataframe
    # # result["test_df"] = result["test_df"][~result["test_df"].index.duplicated(keep='first')]
    # # remove dates from the training/testing sets & convert to float32
    result["X"] = result["X"][:, :, :len(feature_columns)].astype(np.float32)

    return result


def create_model(sequence_length, n_features, units=256, cell=LSTM, n_layers=2, dropout=0.3,
                 loss="mean_absolute_error", optimizer="rmsprop", bidirectional=False):
    model = Sequential()
    for i in range(n_layers):
        if i == 0:
            # first layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True),
                                        batch_input_shape=(None, sequence_length, n_features)))
            else:
                model.add(cell(units, return_sequences=True, batch_input_shape=(None, sequence_length, n_features)))
        elif i == n_layers - 1:
            # last layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=False)))
            else:
                model.add(cell(units, return_sequences=False))
        else:
            # hidden layers
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True)))
            else:
                model.add(cell(units, return_sequences=True))
        # add dropout after each layer
        model.add(Dropout(dropout))
    model.add(Dense(1, activation="linear"))
    model.compile(loss=loss, metrics=["mean_absolute_error"], optimizer=optimizer)
    return model


if __name__ == '__main__':
    result = preprocess_data(ticker='BTC')
    result = preprocess_data_test(ticker='BTC', column_scaler=result["column_scaler"])
    x=1
