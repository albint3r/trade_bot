# Import
# Hint Types
from dataclasses import dataclass, field
from pandas import DataFrame
# Class Object
from abc import ABC, abstractmethod
# Stocks
from binance import Client
# Plots
from plotting.stock_plots import StockPlots


@dataclass
class TradeBotABC(ABC):

    client: Client = field(init=False, repr=False)
    config: dict = field(init=False, default_factory=dict, repr=False)
    df: DataFrame = field(repr=False, default=None)
    _current_crypto = None
    _current_interval = None
    _current_start_date = None
    _json_data: object = field(repr=False, default=None)
    _plot: StockPlots = field(init=False, repr=False, default=None)

    def __post_init__(self):
        self._plot = StockPlots()

    @abstractmethod
    def create_client(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def plot(self):
        pass

    def set_stock_plots(self):
        self._plot = StockPlots()

    def from_object(self, config_object: object) -> None:
        """Set the configuration Values fot the trading bot

        Parameters:
        -----------
        config_object: Object:
            Object Class that contains the General Configuration for the TradeBots.

        Return:
        ----------
        None
        """
        self.config = vars(config_object())


