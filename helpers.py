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

def create_signature(data):
    signature = hmac.new(bytes(API_SECRET, 'UTF-8') , urlencode(data).encode(), hashlib.sha256).hexdigest()
    return signature

def place_order(symbol, price, side):
    URL = API_URL + "order"

    DATA = {
        "symbol": symbol,
        "type": "LIMIT_MAKER", #STOP_LOSS & STOP_LOSS_LIMIT orders not allowed for chosen trading pair
        "side": side,
        "price": price,
        "quantity": 0.001,
        "timestamp": round(time.time() * 1000)
    }
    
    signature = create_signature(DATA)
    DATA["signature"] = signature
    
    try:
        response = requests.post(url = URL, headers=HEADERS, data = DATA)
    
    except requests.exceptions as e:
        print(e.response.text)
    
    if response.status_code == 200:
        print("** ", side, " Order placed at ", str(price), " **")

def cancel_all_orders(symbol):
    URL = API_URL + "openOrders"
    DATA = {
        "symbol": symbol,
        "timestamp": round(time.time() * 1000)
    }
    
    signature = create_signature(DATA)
    DATA["signature"] = signature
    
    try:
        response = requests.delete(url = URL, headers=HEADERS, data = DATA)
    except requests.exceptions as e:
        print(e.response.text)
        
    if response.status_code == 200:
        print("** Existing orders cancelled **")
