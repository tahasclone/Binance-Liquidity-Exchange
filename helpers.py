import config
import requests
import time
import hmac
from urllib.parse import urlencode
import hashlib

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET

API_URL = "https://testnet.binance.vision/api/v3/"

HEADERS = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }


def place_order(symbol, price, side):
    URL = API_URL + "order"

    DATA = {
        "symbol": symbol,
        "type": "STOP_LOSS" if side=="SELL" else "TAKE_PROFIT",
        "side": side,
        "stopPrice": price,
        "quantity": 1,
        "timestamp": round(time.time() * 1000)
    }
    
    signature = hmac.new(bytes(API_SECRET, 'UTF-8') , urlencode(DATA).encode(), hashlib.sha256).hexdigest()
    DATA["signature"] = signature
    
    response = requests.post(url = URL, headers=HEADERS, data = DATA)
    
    return response

def cancel_all_orders(symbol):
    URL = API_URL + "openOrders"
    DATA = {
        "symbol": symbol,
        "timestamp": round(time.time() * 1000)
    }
    
    signature = hmac.new(bytes(API_SECRET, 'UTF-8') , urlencode(DATA).encode(), hashlib.sha256).hexdigest()
    DATA["signature"] = signature
    
    response = requests.delete(url = URL, headers=HEADERS, data = DATA)
    
    return response


if __name__ == "__main__":
    response = place_order("BTCUSDT", 19700.0, "BUY")
    print(response.text)