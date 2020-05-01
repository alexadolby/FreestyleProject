
import os
from dotenv import load_dotenv
from datetime import date
from app import APP_ENV
from app.email_service import send_email
import json

load_dotenv()

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

MY_NAME = os.getenv("MY_NAME", default="Player 1")

if __name__ == "__main__":

    if APP_ENV == "development":
        symbol = input("PLEASE INPUT A STOCK SYMBOL: ")
        
    html = ""
    html += f"<h3>Good Evening, {MY_NAME}!</h3>"

    html += "<h4>Today's Date</h4>"
    html += f"<p>{date.today().strftime('%A, %B %d, %Y')}</p>"

    html += f"<h4>Market Data for {symbol}</h4>" #DEFINE SYMBOL
    html += "<ul>"
    #for hourly in weather_results["hourly_forecasts"]:
        #html += f"<li>{hourly['timestamp']} | {hourly['temp']} | {hourly['conditions'].upper()}</li>"
    html += "</ul>"

    send_email(subject="[Market Daily] My Closing Report", html=html)