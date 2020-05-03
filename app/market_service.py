import os
import json
from pprint import pprint

import requests
from dotenv import load_dotenv

from app import APP_ENV

load_dotenv()

def line():
        print("-" * 30)

def to_usd(my_price):
    return "${0:,.2f}".format(my_price) 

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

#User inputs the stocks they want to follow
while True:
    symbol = input("Please input a stock symbol, when finished type DONE: ")
    if symbol == "DONE":
        break

# GET STOCKS 

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
response = requests.get(request_url)
parsed_response = json.loads(response.text)

#GET IT SO USER SEES DATA FOR ALL INPUTTED STOCKS

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

#Print stock data for user inputted symbols on terminal
line()
print(f"SELECTED SYMBOL: {symbol}")
line()
print("REQUESTING STOCK MARKET DATA...")
line()
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")