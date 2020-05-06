import os
import json
from pprint import pprint
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import requests
from datetime import date
from dotenv import load_dotenv
from app.email_service import send_email

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
if APP_ENV == "development":
        symbol1 = input("Please input a stock symbol(EX: MSFT): ")
        second_symbol1 = input("Please input a stock symbol(EX: AMZN): ")
        third_symbol1 = input("Please input a stock symbol(EX: DIS): ") # invoke with custom params
else:
        symbol1 = "MSFT"
        second_symbol1 = "AMZN"
        third_symbol1 = "DIS"

symbol = symbol1 #"MSFT"
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
response = requests.get(request_url)
parsed_response = json.loads(response.text)
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())
latest_day = dates[0] #Today's date to find open and close for the day 
latest_open = tsd[latest_day]["1. open"] 
latest_close = tsd[latest_day]["4. close"]

dict = {
    "value": symbol,
    "start_price": latest_open,
    "end_price": latest_close
}

#print(dict)
#breakpoint

second_symbol = second_symbol1 #"AMZN"
request_url2 = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={second_symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
response2 = requests.get(request_url2)
parsed_response2 = json.loads(response2.text)
last_refreshed2 = parsed_response2["Meta Data"]["3. Last Refreshed"]
tsd2 = parsed_response2["Time Series (Daily)"]
dates2 = list(tsd2.keys())
latest_day2 = dates2[0] #Today's date to find open and close for the day 
latest_open2 = tsd2[latest_day2]["1. open"] 
latest_close2 = tsd2[latest_day2]["4. close"]

dict2 = {
    "value": second_symbol,
    "start_price": latest_open2,
    "end_price": latest_close2
}

#print(dict2)
#breakpoint 

third_symbol = third_symbol1 #"DIS"
request_url3 = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={third_symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
response3 = requests.get(request_url3)
parsed_response3 = json.loads(response3.text)
last_refreshed2 = parsed_response3["Meta Data"]["3. Last Refreshed"]
tsd3 = parsed_response3["Time Series (Daily)"]
dates3 = list(tsd3.keys())
latest_day3 = dates3[0] #Today's date to find open and close for the day 
latest_open3 = tsd3[latest_day3]["1. open"] 
latest_close3 = tsd3[latest_day3]["4. close"]

dict3 = {
    "value": third_symbol,
    "start_price": latest_open3,
    "end_price": latest_close3
}

#print(dict3)
#breakpoint 


if __name__ == "__main__":
    example_subject = "Market Closing " #This tests to make sure the email capabilities are working correctly

    example_html = f""" 
    <h2>Good Evening, here are your daily closing prices!</h3>
    <h4>Today's Date</h4>
    <p>{date.today().strftime('%A, %B %d, %Y')}</p>
    <h2>My Stocks</h4>
    <h4>{symbol}</H4>
        <p>Opening Price: {to_usd(float(latest_open))}</p>
        <p>Closing Price: {to_usd(float(latest_close))}</p>
    <h4>{second_symbol}</H4>
        <p>Opening Price: {to_usd(float(latest_open2))}</p>
        <p>Closing Price: {to_usd(float(latest_close2))}</p>
    <h4>{third_symbol}</H4>
        <p>Opening Price: {to_usd(float(latest_open3))}</p>
        <p>Closing Price: {to_usd(float(latest_close3))}</p>
    <h2>Have a good night!</h2>
    """

    send_email(example_subject, example_html)
