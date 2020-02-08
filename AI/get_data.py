import requests
import json


r = requests.get('https://finnhub.io/api/v1/forex/candle?symbol=OANDA:EUR_USD&resolution=D&from=1549584000&to=Unix.Now&token=bovgj2nrh5r90eafkcu0')
print(json.dumps(r.json(), indent=4))