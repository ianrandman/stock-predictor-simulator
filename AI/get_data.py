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
        for file_name in os.listdir(candle_data_path):
            df = pd.read_csv(candle_data_path + file_name, index_col=0)
            crypto_candles.append(df)
    else:
        os.makedirs(candle_data_path)

        base_url = 'https://finnhub.io/api/v1/crypto/candle'

        request_parameters = dict()
        # request_parameters['format'] = 'csv'
        request_parameters['resolution'] = 'D'
        request_parameters['from'] = '1549584000'  # 02/08/2019 @ 12:00am (UTC)
        request_parameters['to'] = '1581120000'  # 02/08/2020 @ 12:00am (UTC)
        request_parameters['token'] = api_key

        for index, row in symbols.head().iterrows():
            market = row['markets']
            symbol = row['symbols']

            request_parameters['symbol'] = symbol
            r = requests.get(base_url, params=request_parameters)
            candles = pd.DataFrame.from_dict(r.json())
            candles.to_csv(candle_data_path + market + '.csv')
            crypto_candles.append(candles)

            #
            #
            #
            # with open(data_file_path, 'a', encoding='utf-8') as output:
            #     # output.write("# this file contains all the data from the " + subreddit_name + " to be tested\n# subreddit_name, title\n\n")
            #
            #     post_num = 1
            #     for submission in reddit.subreddit(subreddit_name).top(time_filter='all', limit=limit):
            #         data = submission.selftext + ' '
            #         for comment in submission.comments.list():
            #             if isinstance(comment, MoreComments):
            #                 continue
            #
            #             data += comment.body + ' '
            #
            #         data = data.replace('\n', ' ')
            #         data = data.replace('\r', ' ')
            #
            #         output.write(submission.subreddit_name_prefixed + ',' + data + '\n')
            #
            #         print("Post", post_num, "from", subreddit_name, "downloaded")
            #
            #         post_num += 1



def file_list(file_name):
    """
    This function opens a file and returns it as a list.
    All new line characters are stripped.
    All lines that start with '#' are considered comments and are not included.
    :param file_name: the name of the file to be put into a list
    :return: a list containing each line of the file, except those that start with '#'
    """

    f_list = []
    with open(file_name, encoding='utf-8') as f:
        for line in f:
            if line[0] != '#' and line[0] != '\n' and len(line[0]) > 0:
                f_list.append(line.strip('\n'))
    return f_list


# def save_posts(subreddit_name, limit):
#     """
#     From a specified subreddit, retrieve a specified number of posts from top of all tim. Save them to a file in the
#     data folder as [subreddit_name].txt, where each line is in the format
#     (subreddit_name, [concatenation of comments from post]).
#     :param subreddit_name: the subreddit to get posts from
#     :param limit: the number of posts to get
#     :return: none
#     """
#
#     data_file_path = DATA_PATH + subreddit_name + '.txt'
#
#     if os.path.isfile(data_file_path):
#         os.remove(data_file_path)
#
#     with open(data_file_path, 'a', encoding='utf-8') as output:
#         output.write("# this file contains all the data from the " + subreddit_name + " to be tested\n# subreddit_name, title\n\n")
#
#         post_num = 1
#         for submission in reddit.subreddit(subreddit_name).top(time_filter='all', limit=limit):
#             data = submission.selftext + ' '
#             for comment in submission.comments.list():
#                 if isinstance(comment, MoreComments):
#                     continue
#
#                 data += comment.body + ' '
#
#             data = data.replace('\n', ' ')
#             data = data.replace('\r', ' ')
#
#             output.write(submission.subreddit_name_prefixed + ',' + data + '\n')
#
#             print("Post", post_num, "from", subreddit_name, "downloaded")
#
#             post_num += 1


def split_data():
    """
    Split data from all subreddits (read in from that subreddit's data file) into training, development, and testing.
    The splits for training, development, and testing are 50%, 25%, 25%, respectively.
    Save each of the splits to file, where each line is in the format (subreddit_name, [concatenation of comments
    from post]).
    :return: none
    """

    training_data_file = open(DATA_PATH + '/training_data.txt', 'w', encoding='utf-8')
    development_data_file = open(DATA_PATH + '/development_data.txt', 'w', encoding='utf-8')
    test_data_file = open(DATA_PATH + '/testing_data.txt', 'w', encoding='utf-8')

    training_data, development_data, test_data = list(), list(), list()

    for subreddit_name in subreddit_names:
        data = np.asarray(file_list(DATA_PATH + subreddit_name + '.txt'))
        random.shuffle(data)

        train, dev, test = np.split(data, [int(0.5 * len(data)), int(0.75 * len(data))])

        training_data.extend(train)
        development_data.extend(dev)
        test_data.extend(test)

    random.shuffle(training_data)
    random.shuffle(development_data)
    random.shuffle(test_data)

    for post in training_data:
        training_data_file.write(post + '\n')

    for post in development_data:
        development_data_file.write(post + '\n')

    for post in test_data:
        test_data_file.write(post + '\n')

    training_data_file.close()
    development_data_file.close()
    test_data_file.close()


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
