import os
import json
from pprint import pprint

import requests
from dotenv import load_dotenv

from app import APP_ENV

load_dotenv()

def line():
        print("-" * 30)

# format price values
def to_usd(my_price):
    return "${0:,.2f}".format(my_price) 

#Use to get Alpha Vantage stock data
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

#User inputs the stocks they want to follow
while True:
    symbol = input("Please input a stock symbol, when finished type DONE: ")
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    tsd = parsed_response["Time Series (Daily)"]

    dates = list(tsd.keys())

    latest_day = dates[0] #Today's date to find open and close for the day 

    latest_open = tsd[latest_day]["1. open"] 
    latest_close = tsd[latest_day]["4. close"]
    
    #take user inputs and create a dictionary to pull the data from for the daily email
    dict = {
        "value": symbol,
        "start_price": latest_open,
        "end_price": latest_close
    }
    #end loop once user is finished with inputs
    if symbol == "DONE":
        break

#Call and print dictionary data for all user inputs in terminal
for k, v in dict.items():   
    line()
    print(f"SELECTED SYMBOL: {symbol}")
    line()
    print(f"TODAY: {last_refreshed}")
    print(f"TODAY'S OPEN:{to_usd(float(latest_open))}")
    print(f"TODAY'S CLOSE: {to_usd(float(latest_close))}")
 