import os
import json
from pprint import pprint
from datetime import date
from app import APP_ENV
from app.email_service import send_email
import requests
from dotenv import load_dotenv
from app import APP_ENV

load_dotenv()

def line():
        print("-" * 30)

#format price 
def to_usd(my_price):
    return "${0:,.2f}".format(my_price) 

#Use to get Alpha Vantage data
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
MY_NAME = os.getenv("MY_NAME", default="User") #Get users name for email

if __name__ == "__main__":

    #User inputs the stocks they want to follow
    while True:
        symbol = input("Please input a stock symbol, when finished type DONE: ")
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(request_url)
        parsed_response = json.loads(response.text)

        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

        tsd = parsed_response["Time Series (Daily)"]

        dates = list(tsd.keys())
        
        latest_day = dates[0] # todays date for latest open and close

        latest_open = tsd[latest_day]["1. open"]
        latest_close = tsd[latest_day]["4. close"]

        #create dictionary of user inputted stock information to call later in the email
        dict = {
            "value": symbol,
            "start_price": latest_open,
            "end_price": latest_close
        }

        if symbol == "DONE": #break once user is done 
            break

    # GET STOCKS 

    #Print stock data for user inputted symbols on terminal
    for k, v in dict.items():   
        line()
        print(f"SELECTED SYMBOL: {symbol}")
        line()
        print(f"TODAY: {last_refreshed}")
        print(f"TODAY'S OPEN:{to_usd(float(latest_open))}")
        print(f"TODAY'S CLOSE: {to_usd(float(latest_close))}")

    #send user closing report with customized information, based on the data printed in the terminal 
    closing_report = f"""
    <h3>Good Evening, here are your daily closing prices!</h3>
    <h4>Today's Date</h4>
    <p>{date.today().strftime('%A, %B %d, %Y')}</p>
    """

    send_email(subject="[Market Daily] My Closing Report", html=closing_report)
 