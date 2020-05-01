import os
import json
from pprint import pprint

import requests
from dotenv import load_dotenv

from app import APP_ENV

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")