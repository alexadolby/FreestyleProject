import pytest
import os
import datetime 
import json 
import requests

from app.market_service import to_usd

def test_to_usd():
     # apply to USD formatting
    result = to_usd(3.50)
    assert result == "$3.50"

    # display two decimal places
    result = to_usd(3.5)
    assert result == "$3.50"

    # round to two decimal places
    result = to_usd(3.666)
    assert result == "$3.67"

    # display thousand separators
    result = to_usd(111222333.45)
    assert result == "$111,222,333.45"