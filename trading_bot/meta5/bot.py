# Import
# Hint Types
from dataclasses import dataclass, field
# Data Type Imports
from pandas import DataFrame
import json
# Stocks
import MetaTrader5 as mt5
# Math and Ds
import pandas as pd
import numpy as np
# Errors
from trading_bot.errors import MissingConfigError, NoExistClientError
# Plots
from plotting.stock_plots import StockPlots
# Abstract Class
from trading_bot.abstrac_class import TradeBotABC


@dataclass
class MetaTraderBot(TradeBotABC):

    def init(self):
        pass

    def login(self):
        pass

    def create_client(self):
        pass

    def run(self):
        pass

    def set_stock_plots(self):
        pass

    def plot(self):
        pass
