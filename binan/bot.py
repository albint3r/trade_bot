# Import
# Hint Types
from dataclasses import dataclass, field
# System
# Stocks
import pandas as pd
from pandas import DataFrame
from binance import Client
# Class Object
from abc import ABC, abstractmethod
# Errors
from .errors import MissingConfigError, NoExistClientError


@dataclass
class TradeBot(ABC):
    client: Client = field(init=False, repr=False)
    config: dict = field(init=False, default_factory=dict, repr=False)

    @abstractmethod
    def create_client(self):
        pass

    def from_object(self, config_object):
        self.config = vars(config_object)

    @abstractmethod
    def run(self):
        pass


@dataclass
class BinanceCryptoTrading(TradeBot):
    json_data: object = field(repr=False, default=None)
    df: DataFrame = field(repr=False, default=None)

    def create_client(self, api_key: str = None, secret_key: str = None) -> None:
        if self.config:
            self.client = Client(api_key or self.config['API_KEY'], secret_key or self.config['SECRET_KEY'])
        else:
            raise MissingConfigError(self.config)

    def create_hist_dataframe(self) -> None:

        columns = ['open_time', 'open', 'high', 'low',
                   'close', 'volume', 'close_time', 'quote_asset_volume',
                   'n_trades', 'tb_base_volume', 'tb_quote_volume', 'ignore']

        if self.json_data:
            self.df = pd.DataFrame(self.json_data, columns=columns)
        else:
            raise NoExistClientError()

    def clean_data(self):

        to_units = 1000
        columns_types = {'open': 'float64',
                         'high': 'float64',
                         'low': 'float64',
                         'close': 'float64',
                         'volume': 'float64',
                         'quote_asset_volume': 'float64',
                         'tb_base_volume': 'float64',
                         'tb_quote_volume': 'float64',
                         'ignore': 'float64'}

        self.df = (self.df
                   .assign(open_time=lambda x: pd.to_datetime(x.open_time / to_units, unit='s'),
                           close_time=lambda x: pd.to_datetime(x.close_time / to_units, unit='s'),
                           )
                   .astype(columns_types)
                   )
        print(f'The DataFrame is Clean Now!')

    def get_historical(self, currency_pair: str, client_time_interval, start_date: str) -> None:
        self.json_data = self.client.get_historical_klines(currency_pair, client_time_interval, start_date)

    def interval(self, time_interval: str) -> str:

        match time_interval:
            case 'hour_1':
                return self.client.KLINE_INTERVAL_1HOUR
            case 'hour_4':
                return self.client.KLINE_INTERVAL_4HOUR
            case 'hour_12':
                return self.client.KLINE_INTERVAL_12HOUR
            case 'day_1':
                return self.client.KLINE_INTERVAL_1DAY
            case 'day_3':
                return self.client.KLINE_INTERVAL_3DAY
            case 'week_1':
                return self.client.KLINE_INTERVAL_1WEEK
            case 'month_1':
                return self.client.KLINE_INTERVAL_1MONTH

    def run(self):
        pass
