### Grab stocks from api, occasionally used to refresh repo and ensure tickers are being predicted
### use secrets.txt
import requests
import json 
import os

api_endpoint = os.environ.get('API_ENDPOINT')
if api_endpoint is None:
  print("SET API ENDPOINT")
  quit(1)

r = requests.get(api_endpoint)
stocks_data = r.json()
file_name = 'config.json'
with open('config.json') as json_file:
  data = json.load(json_file)

data["stocks"] = stocks_data.get('data')
with open(file_name, 'w') as outfile:
  json.dump(data, outfile)
