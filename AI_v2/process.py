from parameters import *
from datetime import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Qt5Agg')


def calculate_percent_change(open, close):
    return 100 * (close - open) / open


def load_data(interval=data_interval, train=True):
    assert interval % 60 == 0

    if train:
        original_df = pd.read_csv('data/BTC_60.csv')
        num_rows_to_skip = int(interval / 60)  # how many rows until the start of the next interval
    else:
        original_df = pd.read_csv('data/new_BTC_3600.csv')
        num_rows_to_skip = int(interval / 3600)  # how many rows until the start of the next interval

    dfs = list()

    print('Loading data...')
    for start_i in tqdm(range(num_rows_to_skip)):
        # ensure all intervals have the same number of rows
        temp_original_df = original_df.truncate(before=start_i,
                                                after=len(original_df) -
                                                      (len(original_df) - start_i) % num_rows_to_skip - 1).reset_index(drop=True)

        # create a df with each row representing an interval
        df = temp_original_df.iloc[0::num_rows_to_skip, :].reset_index(drop=True)

        # sum the volume for each interval
        df['volume'] = temp_original_df['volume'].values.reshape(-1, num_rows_to_skip).sum(1)

        # the close of an interval is the open of the next
        df['close'] = df['open'].shift(-1)

        # add hour and minute to the df
        df['hour'] = df['time'].apply(lambda x: datetime.fromtimestamp(x).hour)
        df['minute'] = df['time'].apply(lambda x: datetime.fromtimestamp(x).minute)

        df.dropna(inplace=True)

        dfs.append(df)

        # df['percent_change'] = df[['open', 'close']].apply(lambda x: calculate_percent_change(*x), axis=1)
        # df['percent_change_positive'] = df['percent_change'].apply(lambda x: int(x > 0))
        #
        # df_grouped = df.groupby(['hour', 'minute'])
        #
        # group_to_percent_positive = dict()
        # for group in df_grouped.groups:
        #     group_to_percent_positive[group] = df_grouped.get_group(group)['percent_change_positive'].mean()
        #
        #
        #
        # # dictionary = {1: 27, 34: 1, 3: 72, 4: 62, 5: 33, 6: 36, 7: 20, 8: 12, 9: 9, 10: 6, 11: 5,
        # #               12: 8, 2: 74, 14: 4, 15: 3, 16: 1, 17: 1, 18: 1, 19: 1, 21: 1, 27: 2}
        # plt.bar([str(key) for key in group_to_percent_positive.keys()], group_to_percent_positive.values(), color='g')
        # plt.show()

        # time_with_max = max(group_to_percent_positive, key=lambda x: group_to_percent_positive[x])
        # max_percent = group_to_percent_positive[time_with_max]
        #
        # print(f'Time with max: {time_with_max}')
        # print(f'Max: {max_percent}')

    x = 1
    # return dfs
    total_df = pd.concat(dfs, join='inner')
    total_df = total_df.sort_values('time').reset_index(drop=True)
    return total_df, dfs


if __name__ == '__main__':
    load_data()
