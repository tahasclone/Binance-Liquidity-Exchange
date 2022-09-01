import config
import requests
import json
import time

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET

API_URL = "https://testnet.binance.vision/api/v3/"
auth = requests.HTTPBasicAuth(API_KEY, API_SECRET)

def place_bid_order(symbol, price):
    URL = API_URL + "order"
    DATA = {
        "symbol": symbol,
        "type": "STOP_LOSS",
        "side": "BUY",
        "stopPrice": price,
        "quantity": 1,
        "timestamp": round(time.time() * 1000),
        "signature": "" # HMAC SHA256 of secret key and total params
    }
    
    response = requests.post(url = URL, data = DATA, auth=auth)
    
    return response
    
def place_ask_order(symbol, price):
    pass

def cancel_bid_order(symbol, orderId):
    pass

def cancel_ask_order(symbol, orderId):
    pass

def cancel_all_orders(symbol):
    # test if cancel all orders api can be used to cancel both bid and ask orders
    pass