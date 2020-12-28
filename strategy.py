# -*- coding: utf-8 -*-
import time
import talib
from datetime import datetime as dt, timezone as tz, timedelta as delta

import pandas as pd
from botter import Botter

class Strategy:

    def __init__(self, Botter):
        self._exchange = Botter._exchange
        self._logger = Botter._logger
        self._config = Botter._config

    def run(self, ticker, orderbook, position, balance, candle):
        # here's your logic
        df = candle.iloc[-30:]
        print(df)
        
        df['ema1'] = talib.EMA(df['close'], timeperiod=self._config["SMA"])
        df['ema2'] = talib.EMA(df['close'], timeperiod=self._config["LMA"])
        df['diff'] = df.ema1 - df.ema2

        print('{} short term ema: {}, {} long term ema: {}'.format(self._config["SYMBOL"], df.iloc[-1]['ema1'], self._config["SYMBOL"], df.iloc[-1]['ema2']))
        print('{} previous diff: {}, {} present diff: {}'.format(self._config["SYMBOL"], df.iloc[-2]['diff'], self._config["SYMBOL"], df.iloc[-1]['diff']))
        print('QTY: {}'.format(self._config["QTY"]))
        qty = self._config["QTY"]
        

        """
        if df.iloc[-2]['diff'] < 0 and df.iloc[-1]['diff'] >= 0:
            order = self._exchange.market_order('buy', qty)
            self._logger.info('Golden Cross appeared {}'.format(order))
        elif df.iloc[-2]['diff'] > 0 and df.iloc[-1]['diff'] <= 0:
            order = self._exchange.market_order('sell', qty)
            self._logger.info('Dead Cross appeared {}'.format(order))
        """

