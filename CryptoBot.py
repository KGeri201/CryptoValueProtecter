#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import FALSE
import yaml
import logging
import websockets
from enum import Enum
from time import sleep
from threading import Thread
from binance.client import Client

# default values
api_key = None
api_secret = None

currency = "EUR"

time_to_wait = 24
time_unit = "hour"

sell_threshold = 0
trade_threshold = 0

doomsdaymeasures = False

start_website = False

logging_level = 3
debug = False


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

def calculateTimeToSleep(time_unit):
    if time_unit == "second":
        return time_to_wait * 1
    elif time_unit == "minute":
        return time_to_wait * 60
    elif time_unit == "hour":
        return time_to_wait * 60 * 60
    else:
        msg = "Unit of time is not valid! Using default value."
        logger.warning(msg)
        print(msg)

def website():
    pass


if __name__ == "__main__":
    # Initialise logger
    logging.basicConfig(filename = "cryptobot.log",
                        filemode = "a",
                        format = "%(levelname)s %(asctime)s - %(message)s", 
                        level = logging_level * 10)
    logger = logging.getLogger()

    # Read config
    try:
        config = yaml.load(open(r'config.yaml'), Loader=yaml.FullLoader)
        if "api_key" in config.keys():
            api_key = config["api_key"]
        if "api_secret" in config.keys():
            api_secret = config["api_secret"]
        if "currency" in config.keys():
            currency = config["currency"]
        if "time_to_wait" in config.keys():
            time_to_wait = config["time_to_wait"]
        if "time_unit" in config.keys():
            time_unit = config["time_unit"]
        if "sell_threshold" in config.keys():
            sell_threshold = config["sell_threshold"]
        if "trade_threshold" in config.keys():
            trade_threshold = config["trade_threshold"]
        if "doomsdaymeasures" in config.keys():
            doomsdaymeasures = config["doomsdaymeasures"]
        if "start_website" in config.keys():
            start_website = config["start_website"]
        if "logging_level" in config.keys():
            logging_level = config["logging_level"]
        if "debug" in config.keys():
            debug = config["debug"]
        time_to_wait = calculateTimeToSleep(time_unit)
        #api_key = config["api_key_test"]
        #api_secret = config["api_secret_test"]time_unit
    except Exception as e:
        print(e)
    except:
        msg = "No config file could be opened! Default values will be used!"
        logger.warning(msg)
        print(msg)
    
    # Website
    try:
        if start_website:
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
        cryptobot()
    except KeyboardInterrupt:
        msg = "Keyboardinterrupt detected"
        logger.warning(msg)
        print(msg)
    except Exception as e:
        logger.error(e)
        print(e)
    finally:
        msg = "CryptoBot was successfuly terminated"
        logger.info(msg)
        print(msg)
