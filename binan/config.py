import os


class Config(object):

    def __init__(self):
        self.API_KEY = os.getenv('BINANCE_API_KEY')
        self.SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
