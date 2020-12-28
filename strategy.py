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
        df = candle
        print(df)
        
        order = self._exchange.market_order('buy', qty) 
        order = self._exchange.market_order('sell', qty)

