import os
import time
from tensorflow.keras.layers import LSTM

# Window size or the sequence length
N_STEPS = 50
# Lookup step, 1 is the next day
LOOKUP_STEP = 15

# # whether to scale feature columns & output price as well
SCALE = True
# scale_str = f"sc-{int(SCALE)}"
# # whether to shuffle the dataset
# SHUFFLE = True
# shuffle_str = f"sh-{int(SHUFFLE)}"
# # whether to split the training/testing set by date
# SPLIT_BY_DATE = False
# split_by_date_str = f"sbd-{int(SPLIT_BY_DATE)}"
# test ratio size, 0.2 is 20%
TEST_SIZE = 0.2
# features to use
FEATURE_COLUMNS = ['low', 'high', 'open', 'volume', 'hour', 'minute']
data_granularity = 60
data_interval = 1 * 60 * 60  # 1 hour

### model parameters

N_LAYERS = 2
# LSTM cell
CELL = LSTM
# 256 LSTM neurons
UNITS = 256
# 40% dropout
DROPOUT = 0.4
# whether to use bidirectional RNNs
BIDIRECTIONAL = False

### training parameters

# mean absolute error loss
# LOSS = "mae"
# huber loss
LOSS = "huber_loss"
OPTIMIZER = "adam"
BATCH_SIZE = 64
EPOCHS = 500

ticker = "BTC"
ticker_data_filename = os.path.join("data", f"{ticker}_{data_granularity}.csv")
# model name to save, making it as unique as possible based on parameters
model_name = f"{ticker}_{data_interval}-\
{LOSS}-{OPTIMIZER}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"
if BIDIRECTIONAL:
    model_name += "-b"
