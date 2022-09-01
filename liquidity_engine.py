import websocket, json, config

TRADING_PAIR = "btcusdt"
TIME_INTERVAL = "1m"

SOCKET = f'wss://stream.binance.com:9443/ws/'+TRADING_PAIR+'@kline_'+TIME_INTERVAL

def on_open(ws):
    print("***Opened Connection***")
    
def on_close(ws):
    print("***Closed Connection***")
    
def on_message(ws, message):
    pass

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()