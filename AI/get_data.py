import requests
import json

with open('./api_key.txt', 'r') as f:
    api_key = f.readline()

r = requests.get('https://finnhub.io/api/v1/forex/candle?symbol=OANDA:EUR_USD&resolution=D&from=1549584000&to=Unix.Now&token=' + api_key)
print(json.dumps(r.json(), indent=4))