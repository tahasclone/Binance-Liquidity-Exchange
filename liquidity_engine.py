from curses.ascii import CAN
from tkinter.messagebox import CANCEL
import websocket, json, logging
from helpers import place_order, cancel_all_orders

logging.basicConfig(level=logging.DEBUG)

TRADING_PAIR = "btcusdt"
TIME_INTERVAL = "1m" 
CURRENT_PRICE = 0.0
ASK_ORDER_PRICE = 0.0
BID_ORDER_PRICE = 0.0
CANCEL_COUNT=0 # This is being set to not cancel the first comparison of price

SOCKET = f'wss://stream.binance.com:9443/ws/'+TRADING_PAIR+'@kline_'+TIME_INTERVAL


def on_open(ws):
    logging.debug("Opened Connection")
    
def on_close(ws,  close_status_code, close_msg):
    logging.debug("Closed Connection")
    
def on_message(ws, message):
    global CURRENT_PRICE, ASK_ORDER_PRICE, BID_ORDER_PRICE, CANCEL_COUNT

    price_data = json.loads(message)
    COMPARE_PRICE = float(price_data['k']['c'])
    
    # Compare new price with ask & bid order price
    if COMPARE_PRICE > CURRENT_PRICE+100.0 or COMPARE_PRICE < CURRENT_PRICE-100.0:
        logging.debug("Compare price broke bid or ask limits")
        # Cancel existing orders
        if CANCEL_COUNT > 0:
            cancel_order_response = cancel_all_orders(TRADING_PAIR.upper())
            if not cancel_order_response:
                exit()
        else:
            CANCEL_COUNT+=1
        
        # update values of current, bid and ask price
        CURRENT_PRICE = COMPARE_PRICE
        ASK_ORDER_PRICE = CURRENT_PRICE + 100.0 # change value to 20.0 for easier testing purpose
        BID_ORDER_PRICE = CURRENT_PRICE - 100.0
        
        # place new orders
        ask_order_response = place_order(TRADING_PAIR.upper(), ASK_ORDER_PRICE, "SELL")
        bid_order_response = place_order(TRADING_PAIR.upper(), BID_ORDER_PRICE, "BUY")
        
        if not ask_order_response:
            exit()
        if not bid_order_response:
            exit()

    else:
        logging.debug("Compare price has not crossed ask or bid order price")    

if __name__ == '__main__':
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()
