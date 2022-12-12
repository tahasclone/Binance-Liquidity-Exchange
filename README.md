# Python Binance Liquidity Script

## Description
The objective of the assignment is to provide liquidity to an Exchange. This is done by placing open orders and adjusting the price when the market is moving.

We do this by:
- Getting the latest price of a symbol eg. BTCUSDT through a websocket stream
- Placing a bid order at 100$ lesser of the price
- Placing an ask order at 100$ greater than the price
- Constantly monitering the price of the trading pair 
- When the trading pair crosses the bid or ask limit created, we cancel both orders and repeat the process with 2 new orders

## Technology
- The project is a python script which can be run from the terminal. It uses websockets to stream the price of a trading pair and places orders using exchange APIs. 

- In this case we are using Binance's websocket stream for "BTCUSDT" pair and binance testnet apis which can be found on: https://binance-docs.github.io/apidocs/

## Steps to run
1. In order to place orders on the testnet, you require API access. You can generate HMAC_SHA256 Keys from: https://testnet.binance.vision/ by connecting with your github account.
2. Install the project on your local machine.
3. Create a python virtual environment and run " pip install  -r requirements.txt " to have all the required external packages for the project.
4. Create a file called " config.py " and include the API_KEY, API_SECRET generated from the testnet website mentioned above and the API_URL.
5. Now you're good to go! Run the project with " python liquidity_engine.py " and watch the magic happen.

## Improvements for scaling
- Using asyncio 
- Placing multiple orders 
- Using multiple accounts 

## Version
- python 3.6.9
