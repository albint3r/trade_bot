# Imports
# Data Type Imports
from pandas import DataFrame
# Plotting
import mplfinance as mpf
import matplotlib.pyplot as plt
import seaborn as sns


class StockPlots:
    TYPE = 'candle'
    STYLE = 'charles'
    VOLUME = True
    FIGSIZE = (20, 10)

    def plot(self, data: DataFrame, current_crypto: str, n_periods: int = 100):
        mpf.plot(data.tail(n_periods),
                 type=self.TYPE,
                 style=self.STYLE,
                 volume=self.VOLUME,
                 title=f'{current_crypto} Last 100 Days',
                 mav=(20, 40, 200))

    def heatmap(self, data: DataFrame):
        fig, ax = plt.subplots(1, 1, figsize=self.FIGSIZE)
        sns.heatmap(data, annot=True)

    def per_change_barplot(self, data: DataFrame, n_periods: int = 100):
        fig, ax = plt.subplots(1, 1, figsize=self.FIGSIZE)
        sns.barplot(data=data.tail(n_periods), x=data.tail(n_periods).index.date, y='per_change_close', ax=ax)
        ax.set(xlabel='Close Time', ylabel='Percentage Close Change')
        ax.tick_params(axis='x', rotation=90)
