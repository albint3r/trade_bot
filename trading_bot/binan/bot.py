# Import
# Hint Types
from dataclasses import dataclass, field
# Data Type Imports
from pandas import DataFrame
import json
# Class Object
from abc import ABC, abstractmethod
# Stocks
from binance import Client
# Math and Ds
import pandas as pd
import numpy as np
# Errors
from trading_bot.errors import MissingConfigError, NoExistClientError
from trading_bot.abstrac_class import TradeBotABC


@dataclass
class BinanceCryptoTrading(TradeBotABC):
    json_data: object = field(repr=False, default=None)
    df: DataFrame = field(repr=False, default=None)
    current_crypto = None
    current_interval = None
    current_start_date = None

    def actualize_current_trade_view(self, currency_pair: str, client_time_interval: str, start_date: str) -> None:
        self.current_crypto = currency_pair
        self.current_interval = client_time_interval
        self.current_start_date = start_date

    def change_pair(self, currency_pair: str) -> None:
        self.get_historical(currency_pair=currency_pair,
                            client_time_interval=self.current_interval,
                            start_date=self.current_start_date)

    def change_interval(self, interval: str):
        self.get_historical(currency_pair=self.current_crypto,
                            client_time_interval=interval,
                            start_date=self.current_start_date)

    def change_start_date(self, start_date: str) -> None:
        self.get_historical(currency_pair=self.current_crypto,
                            client_time_interval=self.current_interval,
                            start_date=start_date)

    def create_client(self, api_key: str = None, secret_key: str = None) -> None:
        if self.config:
            self.client = Client(api_key or self.config['API_KEY'], secret_key or self.config['SECRET_KEY'])
        else:
            raise MissingConfigError(self.config)

    def create_hist_dataframe(self) -> None:

        columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
                   'n_trades', 'tb_base_volume', 'tb_quote_volume', 'ignore']

        if self.json_data:
            self.df = pd.DataFrame(self.json_data, columns=columns)
        else:
            raise NoExistClientError()

    def clean_data(self) -> None:

        to_units = 1000  # Need to divide the time by this number to convert into Units.
        columns_types = {'open': 'float64', 'high': 'float64', 'low': 'float64',
                         'close': 'float64', 'volume': 'float64', 'quote_asset_volume': 'float64',
                         'tb_base_volume': 'float64', 'tb_quote_volume': 'float64', 'ignore': 'float64'}

        self.df = (self.df
                   .assign(open_time=lambda x: pd.to_datetime(x.open_time / to_units, unit='s'),
                           close_time=lambda x: pd.to_datetime(x.close_time / to_units, unit='s'))
                   .astype(columns_types)
                   .set_index('close_time'))

        print(f'The DataFrame is Clean Now!')

    def get_historical(self, currency_pair: str, client_time_interval: str, start_date: str) -> None:
        self.json_data = self.client.get_historical_klines(currency_pair, client_time_interval, start_date)
        self.actualize_current_trade_view(currency_pair, client_time_interval, start_date)
        self.run()

    def get_all_cryptos(self) -> json:
        return self.client.get_all_tickers()

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

    def run(self) -> None:
        self.create_hist_dataframe()
        self.clean_data()
        self.feature_engineering()

    def feature_engineering(self) -> None:
        self.df = (self.df
                   .assign(time=lambda x: np.arange(len(x.close)),
                           diff_hig_low=lambda x: x.high - x.low,
                           ratio_open_close=lambda x: x.open / x.close,
                           # TODO they made some modification to the feature engineer to identify
                           # TODO What features are most important to get a buy or sell signal.
                           per_change_close=lambda x: ((x.close - x.close.shift(1)) / x.close.shift(1)) * 100,
                           ma20=lambda x: x.close.rolling(window=20).mean(),
                           ma40=lambda x: x.close.rolling(window=40).mean(),
                           ma200=lambda x: x.close.rolling(window=200).mean(),
                           per_change_close_ma2=lambda x: (x.close - x.ma20) / x.ma20 * 100,
                           signal=lambda x: x.per_change_close.gt(0),
                           )
                   .dropna()
                   )

    def plot(self, n_periods: int = 100) -> None:
        self._plot.plot(self.df, self.current_crypto, n_periods)

    def corr_time(self):
        return self.df.loc[:, ['time', 'close']].corr()

    def heatmap(self, corr_tye: str):
        match corr_tye:
            case 'time':
                self._plot.heatmap(self.corr_time())

    def per_change_barplot(self, n_periods: int = 100):
        self._plot.per_change_barplot(self.df, n_periods)
