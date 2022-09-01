import websocket, json
from helpers import place_order, cancel_all_orders

TRADING_PAIR = "btcusdt"
TIME_INTERVAL = "1m" 
CURRENT_PRICE = 0.0
ASK_ORDER_PRICE = 0.0
BID_ORDER_PRICE = 0.0

SOCKET = f'wss://stream.binance.com:9443/ws/'+TRADING_PAIR+'@kline_'+TIME_INTERVAL


def on_open(ws):
    print("***Opened Connection***")
    
def on_close(ws):
    print("***Closed Connection***")
    
def on_message(ws, message):
    global CURRENT_PRICE, ASK_ORDER_PRICE, BID_ORDER_PRICE
    price_data = json.loads(message)
    COMPARE_PRICE = float(price_data['k']['c'])

    # Compare new price with ask order price
    if COMPARE_PRICE > CURRENT_PRICE+100.0:
        print("compare price greater than current price")
        # Cancel existing orders
        cancel_all_orders(TRADING_PAIR) # API FAILING
        
        # update values of current, bid and ask price
        CURRENT_PRICE = COMPARE_PRICE
        ASK_ORDER_PRICE = CURRENT_PRICE + 100.0
        BID_ORDER_PRICE = CURRENT_PRICE - 100.0
        
        # place new orders     
        place_order(TRADING_PAIR, ASK_ORDER_PRICE, "SELL")
        place_order(TRADING_PAIR, BID_ORDER_PRICE, "BUY")
    else:
        print("Compare price has not crossed ask order price")
        

try:
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()
except KeyboardInterrupt:
    ws.close()
    print("Connection Ended")
