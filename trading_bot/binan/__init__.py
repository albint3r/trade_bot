from .bot import BinanceCryptoTrading
from config import Config


def app_factory():
    bbot = BinanceCryptoTrading()
    bbot.from_object(Config)
    bbot.create_client()
    bbot.get_historical('ETHBTC', bbot.interval('day_1'), '1 Jan 2011')
    return bbot
