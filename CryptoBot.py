#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import yaml
import logging
from binance.client import Client

api_key = None
api_secret = None

currency = "EUR"
time_to_wait = 1
logging_level = 3
sell_threshold = 0
trade_threshold = 0
doomsdaymeasures = False

def getBalance(info, all_coins=None):
    balance = []
    for item in info["balances"]:
        if float(item["free"]) > 0 and float(item["free"]) > float(item["locked"]):
        #    if all_coins is not None:
        #        item.update({"value": None})
        #        for coin in all_coins:
        #            if coin["symbol"].find(item["asset"]+currency) != -1:
        #                item["value"] = float(item["free"]) * float(coin["price"])
            balance.append(item)
    return balance

def findBestPriceChangePercentage(client):
    all_tickers = client.get_ticker()
    highest_ticker = all_tickers[0]
    for ticker in all_tickers:
        if ticker["symbol"].find(currency) != -1:
            if float(highest_ticker["priceChangePercent"]) < float(ticker["priceChangePercent"]):
                highest_ticker = ticker
    return highest_ticker

def trade(client, asset):
    best_asset = findBestPriceChangePercentage(client)
    if float(best_asset["priceChangePercent"]) < sell_threshold:
        #order = client.create_test_order(
        #    symbol=asset["asset"]+currency,
        #    side="SELL",
        #    type="MARKET",
        #    quantity=asset["free"])
        #print(order)
        pass
    else:
        print(best_asset)

def main():
    #client = Client(api_key, api_secret, testnet=True)
    client = Client(api_key, api_secret)
    #order = client.order_market_sell(
    #symbol='ETHEUR')
    #print(order)
    #while True:
    assets = getBalance(client.get_account())
    for asset in assets:
        print(asset)
        try:
            ticker = client.get_ticker(symbol=(asset["asset"]+currency))
            print(str(float(ticker["priceChangePercent"]))+" %")
            if float(ticker["priceChangePercent"]) < trade_threshold:
                trade(client, asset)
        except:
            print("No ticker with the current currency was found")
        #time.sleep(time_to_wait * 3600)

 
if __name__ == "__main__":
    logging.basicConfig(filename = "cryptobot.log",
                        filemode = "a",
                        format = "%(levelname)s %(asctime)s - %(message)s", 
                        level = logging_level * 10)
    logger = logging.getLogger()
    try:
        config = yaml.load(open(r'config.yaml'), Loader=yaml.FullLoader)
        api_key = config["api_key"]
        api_secret = config["api_secret"]
        #api_key = config["api_key_test"]
        #api_secret = config["api_secret_test"]
    except:
        msg = "No config file was found!"
        logger.warning(msg)
        print(msg)
    try:
        if (api_key is None or api_secret is None) :
            raise Exception("api_key or api_secret is not set")
        main()
    except KeyboardInterrupt:
        msg = "CryptoBot was manually terminated"
        logger.warning(msg)
        print(msg)
    except Exception as e:
        logger.error(e)
        print(e)
    finally:
        pass
