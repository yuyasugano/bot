# -*- coding: utf-8 -*-
import sys
import ccxt
import time
import json

import logging
from logging import getLogger, StreamHandler, Formatter
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

from datetime import datetime, timedelta, timezone
import calendar

from cryptobot import CryptoBot
args = sys.argv

class Botter:

    def __init__(self, args):
        self._tz = timezone.utc # utc timezone
        self._ts = datetime.now(self._tz).timestamp()

        if len(args) != 3:
            print("number of args does not match")
            exit()

        with open(args[2], "r") as f:
            jsonData = json.load(f)
            self._config = jsonData
            print('Configuration file {} loaded'.format(args[1]))
            print(json.dumps(self._config, sort_keys=True, indent=4))

        # logging configuration
        logger = getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # create file handler
        fh = logging.FileHandler('yourfilename.log')
        fh.setLevel(logging.DEBUG)
        fh_formatter = logging.Formatter('%(levelname)s : %(asctime)s : %(message)s')
        fh.setFormatter(fh_formatter)

        # create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch_formatter = logging.Formatter('%(levelname)s : %(asctime)s : %(message)s')
        ch.setFormatter(ch_formatter)

        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        self._logger = logger

        if "LOG_LEVEL" in self._config:
            if self._config["LOG_LEVEL"] in [
                "CRITICAL",
                "ERROR",
                "WARNING",
                "INFO",
                "DEBUG",
            ]:
                self._logger.setLevel(eval("logging." + self._config["LOG_LEVEL"]))

        self._exchange = CryptoBot(
            symbol = self._config["SYMBOL"],
            apiKey = self._config["APIKEY"],
            secret = self._config["SECRET"],
            logger = self._logger
        )

        # load strategy and generate a class
        module = machinery.SourceFileLoader("Strategy", args[1]).load_module()
        self._Strategy = module.Strategy(self)

        message = "Botter initialized with CryptoBot={}, Config={}".format(args[1], args[2])
        self._logger.info(message)

if __name__ == "__main__":
    tz = timezone.utc
    
    def start():
        bot = Botter(args=args)
        while True:
            try:
                run(Bot=bot)
            except KeyboardInterrupt:
                bot._logger.info("Keyboard Interruption detected, exit the program")
                if len(bot._exchange.open_orders()):
                    bot._exchange.cancel_orders()
                    bot._logger.info("Cancelled the existing orders, please confirm")
                    time.sleep(3)
                exit()
            except Exception as e:
                bot._logger.info("Unknown error occurred, exit the program")
                if len(bot._exchange.open_orders()):
                    bot._exchange.cancel_orders()
                    bot._logger.info("Cancelled the existing orders, please confirm")
                    time.sleep(3)
                exit()

    def run(Bot):
        while True:
            Bot._ts = datetime.now(tz).timestamp()
            balance, candle, orderbook, position, ticker = None, None, None, None, None

            current = time.time()
            try:
                candle = Bot._exchange.ohlcv(symbol=Bot._config["SYMBOL"], timeframe=Bot._config["TIMEFRAME"])
                balance = Bot._exchange.balance()
                ticker = Bot._exchange.ticker(symbol=Bot._config["SYMBOL"])
                orderbook = Bot._exchange.orderbook(symbol=Bot._config["SYMBOL"])
                position = Bot._exchange.position()

            except Exception as e:
                Bot._logger.error("Bot.run() raised an exception: {}".format(e))
                elapsed_time = time.time() - current
                if elapsed_time > Bot._config["INTERVAL"]:
                    Bot._logger.warning(
                        "elapsed_time={0} over interval time={1}".format(
                            elapsed_time, Bot._config["INTERVAL"]
                        )
                    )
                continue

            # invoke the loaded strategy
            Bot._Strategy.run(ticker, orderbook, position, balance, candle)

            elapsed_time = time.time() - current
            interval = Bot._config["INTERVAL"]
            if interval - elapsed_time > 0:
                time.sleep(interval - elapsed_time)
            else:
                time.sleep(1)
                Bot._logger.warning(
                    "elapsed_time={0} over interval time={1}".format(
                        elapsed_time, interval
                    )
                )
    start()

