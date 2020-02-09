from flask import Flask
from flask import request
import datetime
import os
app = Flask(__name__)


def get_supported_stocks():
    supported_stocks = []
    DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../AI/data/'
    candle_data_path = DATA_PATH + 'crypto_candles/'
    for file_name in os.listdir(candle_data_path):
        supported_stocks.append(file_name[:-len('USDT.csv')])
    return supported_stocks


supported_stocks = get_supported_stocks()


def predict(stock, date=datetime.datetime.now(datetime.timezone.utc)):
    """
    Consults trained model to get predicted percentage change for the provided stock
    TODO mock value for now, need to actually consult model
    :param stock: the code of the stock to be evaluated
    :return: predicted percent change, can be positive or negative
    """
    return 5


@app.route("/predict")
def predict_route():
    if request.args.get('stock'):
        stock = request.args.get('stock')
        if stock not in supported_stocks:
            return "Bad request, Invalid stock", 400
        if request.args.get('date'):
            date = request.args.get('date')
            return {"percent_change": predict(stock, date)}
        return {"percent_change": predict(stock)}
    else:
        return "Bad request, Stock not provided", 400


@app.route("/list")
def list_route():
    return {"supported_stocks": supported_stocks}


if __name__ == "__main__":
    app.run()
