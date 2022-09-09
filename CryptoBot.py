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

class Type(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5
    EXCEPTION = 6

# default values
api_key = None
api_secret = None

currency = "EUR"

time_to_wait = 24
time_unit = "hour"

sell_threshold = 0
trade_threshold = 0

doomsdaymeasures = False

monitor = False

logging_level = 2
debug = False

error = None

def log(msg, type=None, display=True):
    if display:
        print(msg)
    if type is Type.DEBUG:
        logger.debug(msg)
    elif type is Type.INFO:
        logger.info(msg)
    elif type is Type.WARNING:
        logger.warning(msg)
    elif type is Type.ERROR:
        logger.error(msg)
    elif type is Type.CRITICAL:
        logger.critical(msg)
    elif type is Type.EXCEPTION:
        logger.exception(msg)

def getBalance(info, all_coins=None):
    balance = []
    for item in info["balances"]:
        if float(item["free"]) > 0 and float(item["free"]) > float(item["locked"]):
            #if all_coins is not None:
            #    item.update({"value": None})
            #    for coin in all_coins:
            #        if coin["symbol"].find(item["asset"]+currency) != -1:
            #            item["value"] = float(item["free"]) * float(coin["price"])
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
        try:
            order = client.create_test_order(
                symbol=asset["asset"]+currency,
                side="SELL",
                type="MARKET",
                quantity=asset["free"])
            log(order, Type.INFO)
            pass
        except Exception as e:
            log(e, Type.ERROR)
    else:
        log(best_asset)

def cryptobot():
    client = Client(api_key, api_secret)
    log("CryptoBot was successfuly started", Type.INFO)
    #if debug:
    #    client = Client(api_key, api_secret, testnet=True)
    #order = client.order_market_sell(
    #symbol='ETHEUR')
    #print(order)
    assets = getBalance(client.get_account())
    log("Balance was loaded.", Type.DEBUG)
    for asset in assets:
        #print(asset)
        try:
            ticker = client.get_ticker(symbol=(asset["asset"]+currency))
            log("Price Change Percentage of " + (asset["asset"]+currency) + " = " + str(float(ticker["priceChangePercent"]))+" %", Type.DEBUG, False)
            if float(ticker["priceChangePercent"]) < trade_threshold:
                trade(client, asset)
        except:
            pass
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
        log("Unit of time is not valid! Using default value.", Type.WARNING)

def website():
    pass


if __name__ == "__main__":
    # print project name
    print("   ___               _     __   __    _          ___         _          _           ")
    print("  / __|_ _ _  _ _ __| |_ __\ \ / /_ _| |_  _ ___| _ \_ _ ___| |_ ___ __| |_ ___ _ _ ")
    print(" | (__| '_| || | '_ \  _/ _ \ V / _` | | || / -_)  _/ '_/ _ \  _/ -_) _|  _/ -_) '_|")
    print("  \___|_|  \_, | .__/\__\___/\_/\__,_|_|\_,_\___|_| |_| \___/\__\___\__|\__\___|_|  ")
    print("           |__/|_|                                                                  ")

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
        if "monitor" in config.keys():
            monitor = config["monitor"]
        if "logging_level" in config.keys():
            logging_level = config["logging_level"]
        if "debug" in config.keys():
            debug = config["debug"]
        time_to_wait = calculateTimeToSleep(time_unit)
        #if debug:
        #    api_key = config["api_key_test"]
        #    api_secret = config["api_secret_test"]
    except Exception as e:
        error = e

    # Initialise logger
    logging.basicConfig(filename = "cryptobot.log",
                        filemode = "a",
                        format = "%(levelname)s %(asctime)s - %(message)s", 
                        level = logging_level * 10)
    logger = logging.getLogger()

    if error is not None:
        log(error, Type.WARNING)

    # Website
    try:
        if monitor:
            ws_thread = Thread(target=website)
            ws_thread.start()
            ws_thread.join()
    except:
        log("No websocket was started!", Type.WARNING)

    # CryptoBot
    try:
        if (api_key is None or api_secret is None) :
            raise Exception("api_key or api_secret is not set")
        cryptobot()
    except KeyboardInterrupt:
        log("Keyboardinterrupt detected", Type.WARNING)
    except Exception as e:
        log(e, Type.ERROR)
    finally:
        log("CryptoBot was successfuly terminated", Type.INFO)
