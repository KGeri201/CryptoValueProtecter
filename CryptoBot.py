#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml
import logging
import websockets
from enum import Enum
from time import sleep
from threading import Thread
from binance.client import Client

# default values
debug = True

api_key = None
api_secret = None

currency = "EUR"
time_to_wait = 24
time_unit = "second"
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

def cryptobot():
    #client = Client(api_key, api_secret, testnet=True)
    client = Client(api_key, api_secret)
    #order = client.order_market_sell(
    #symbol='ETHEUR')
    #print(order)
    assets = getBalance(client.get_account())
    for asset in assets:
        print(asset)
        try:
            ticker = client.get_ticker(symbol=(asset["asset"]+currency))
            print(str(float(ticker["priceChangePercent"]))+" %")
            if float(ticker["priceChangePercent"]) < trade_threshold:
                trade(client, asset)
        except:
            print("Ticker can not be found with the current currency")
    if not debug:
        for seconds in range(time_to_wait):
            sleep(1)

def calculateTimeToSleep(unit = None):
    if unit == "second":
        return time_to_wait * 1
    elif unit == "minute":
        return time_to_wait * 60
    elif unit == "hour":
        return time_to_wait * 60 * 60
    elif unit == "day":
        return time_to_wait * 60 * 60 * 24
    else:
        msg = "No unit for time was defined. It will use seconds."
        logger.warning(msg)
        print(msg)
        return time_to_wait

def website():
    pass


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
        time_to_wait = calculateTimeToSleep("hour")
    except:
        msg = "No config file was found!"
        logger.warning(msg)
        print(msg)
    
    # Website
    try:
        ws_thread = Thread(target=website)
        ws_thread.start()
        ws_thread.join()
    except:
        msg = "No websocket was started!"
        logger.warning(msg)
        print(msg)

    # CryptoBot
    try:
        if (api_key is None or api_secret is None) :
            raise Exception("api_key or api_secret is not set")
        bot_thread = Thread(target=cryptobot)
        bot_thread.start()
        bot_thread.join()
    except KeyboardInterrupt:
        msg = "CryptoBot was manually terminated"
        logger.warning(msg)
        print(msg)
    except Exception as e:
        logger.error(e)
        print(e)
    finally:
        msg = "CryptoBot was successfuly terminated"
        logger.info(msg)
        print(msg)
