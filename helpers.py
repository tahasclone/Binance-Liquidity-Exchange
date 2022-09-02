import config, requests, time, hmac, hashlib, logging, json
from urllib.parse import urlencode

logging.basicConfig(level=logging.DEBUG)

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET

# testnet url
API_URL = "https://testnet.binance.vision/api/v3/"

HEADERS = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

# signature required with data of trade api calls, signature is created with hmac256 of API Secret & querystring of params
def create_signature(data):
    signature = hmac.new(bytes(API_SECRET, 'UTF-8') , urlencode(data).encode(), hashlib.sha256).hexdigest()
    return signature

# function to place orders, data required is symbol, type of order, side ( buy or sell), quantity, timestamp in ms
def place_order(symbol, price, side):
    URL = API_URL + "order"

    DATA = {
        "symbol": symbol,
        "type": "LIMIT_MAKER", #STOP_LOSS & STOP_LOSS_LIMIT orders not allowed for chosen trading pair
        "side": side,
        "price": price,
        "quantity": 1,
        "timestamp": round(time.time() * 1000)
    }
    
    signature = create_signature(DATA)
    DATA["signature"] = signature
    
    try:
        response = requests.post(url = URL, headers=HEADERS, data = DATA)
        response.raise_for_status()
        
        if response.status_code == 200:
            logging.debug(str(side) + " Order placed at " + str(price))
            
            return True
    
    except requests.exceptions.HTTPError as e:
        logging.warning(e.response.text)
        return False
    
    except requests.exceptions.ConnectionError as e:
        logging.error(e)
        return False
        

# function to cancel all existing orders placed by current account
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
        response.raise_for_status()
        
        if response.status_code == 200:
            logging.debug("Existing orders cancelled")
            
            return True

    except requests.exceptions.HTTPError as e:
        logging.warning(e.response.text)
        return False
    
    except requests.exceptions.ConnectionError as e:
        logging.error(e)
        return False