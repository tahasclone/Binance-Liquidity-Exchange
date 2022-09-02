import websocket, json, logging
from helpers import place_order, cancel_all_orders

logging.basicConfig(level=logging.DEBUG)

TRADING_PAIR = "btcusdt"
TIME_INTERVAL = "1m" 
CURRENT_PRICE = 0.0
ASK_ORDER_PRICE = 0.0
BID_ORDER_PRICE = 0.0

SOCKET = f'wss://stream.binance.com:9443/ws/'+TRADING_PAIR+'@kline_'+TIME_INTERVAL


def on_open(ws):
    logging.debug("Opened Connection")
    
def on_close(ws):
    logging.debug("Closed Connection")
    
def on_message(ws, message):
    global CURRENT_PRICE, ASK_ORDER_PRICE, BID_ORDER_PRICE
    price_data = json.loads(message)
    COMPARE_PRICE = float(price_data['k']['c'])

    # Compare new price with ask & bid order price
    if COMPARE_PRICE > CURRENT_PRICE+100.0 or COMPARE_PRICE < CURRENT_PRICE-100.0:
        logging.debug("Compare price broke bid or ask limits")
        # Cancel existing orders
        cancel_response = cancel_all_orders(TRADING_PAIR.upper())
        
        # update values of current, bid and ask price
        CURRENT_PRICE = COMPARE_PRICE
        ASK_ORDER_PRICE = CURRENT_PRICE + 100.0
        BID_ORDER_PRICE = CURRENT_PRICE - 100.0
        
        # place new orders
        ask_order_response = place_order(TRADING_PAIR.upper(), ASK_ORDER_PRICE, "SELL")
        bid_order_response = place_order(TRADING_PAIR.upper(), BID_ORDER_PRICE, "BUY")

    else:
        print("Compare price has not crossed ask order price")
        

try:
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()
except KeyboardInterrupt:
    cancel_all_orders(TRADING_PAIR.upper())
    ws.close()
