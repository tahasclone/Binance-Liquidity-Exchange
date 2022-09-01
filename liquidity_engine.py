import websocket, json
from helpers import place_order, cancel_all_orders

TRADING_PAIR = "BTCUSDT"
TIME_INTERVAL = "1s" 
COMPARE_PRICE = 0.0
CURRENT_PRICE = 0.0
ASK_ORDER_PRICE = 0.0
BID_ORDER_PRICE = 0.0
FIRST_PRICE_SET = False

SOCKET = f'wss://stream.binance.com:9443/ws/'+TRADING_PAIR+'@kline_'+TIME_INTERVAL

def on_open(ws):
    print("***Opened Connection***")
    
def on_close(ws):
    print("***Closed Connection***")
    
def on_message(ws, message):
    global COMPARE_PRICE, CURRENT_PRICE, ASK_ORDER_PRICE, BID_ORDER_PRICE, FIRST_PRICE_SET
    
    price_data = json.loads(message)
    COMPARE_PRICE = price_data['k']['c']
    print("compare price is ", COMPARE_PRICE)
    if FIRST_PRICE_SET:
        # Compare current price with ask & bid orders price
        # if price has past any of the limits set
        # Cancel existing orders
        # place new orders
        # update values of current, bid and ask price
        print("inside first price set loop")
    else:
        CURRENT_PRICE = price_data['k']['c']
        BID_ORDER_PRICE = CURRENT_PRICE - 100
        ASK_ORDER_PRICE = CURRENT_PRICE + 100
        print("current price is ", CURRENT_PRICE) # Not printing, only first print statment gets executed due to frequency of messages
        print("bid order price is ", BID_ORDER_PRICE)
        print("ask order price is ", ASK_ORDER_PRICE)
        FIRST_PRICE_SET = True    
    

try:
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()
except KeyboardInterrupt:
    ws.close()
    print("Connection Ended")