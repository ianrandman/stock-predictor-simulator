from flask import Flask
from flask import request
import datetime
import os

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


supported_stocks = [
       "ADA",
       "ALGO",
       "ANKR",
       "ATOM",
       "BAT",
       "BCHABC",
       "BCHSV",
       "BNB",
       "BTC",
       "BTT",
       "CELR",
       "COCOS",
       "COS",
       "DASH",
       "DOGE",
       "DUSK",
       "ENJ",
       "EOS",
       "ERD",
       "ETC",
       "ETH",
       "FET",
       "FTM",
       "GTO",
       "HOT",
       "ICX",
       "IOST",
       "IOTA",
       "LINK",
       "LTC",
       "MATIC",
       "MITH",
       "NANO",
       "NEO",
       "NPXS",
       "NULS",
       "OMG",
       "ONE",
       "ONG",
       "ONT",
       "PAX",
       "QTUM",
       "TFUEL",
       "THETA",
       "TRX",
       "TUSD",
       "USDC",
       "USDSB",
       "USDS",
       "VET",
       "WAVES",
       "WIN",
       "XLM",
       "XMR",
       "XRP",
       "ZEC",
       "ZIL",
       "ZRX"
     ]


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
            return {"percentChange": predict(stock, date)}
        return {"percentChange": predict(stock)}
    else:
        return "Bad request, Stock not provided", 400


@app.route("/list")
def list_route():
    return {"supportedStocks": supported_stocks}


if __name__ == '__main__':
    app.run(debug=True)
