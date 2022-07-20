from .bot import BinanceCryptoTrading
from .config import Config


def app_factory():
    bbot = BinanceCryptoTrading()
    config = Config()
    bbot.from_object(config)
    bbot.create_client()
    bbot.get_historical('ETHBTC', bbot.interval('day_1'), '1 Jan 2011')
    bbot.create_hist_dataframe()
    bbot.clean_data()
    return bbot
