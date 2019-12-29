from enum import Enum


class Constants:

    main = "Template_indicator_axis"
    adj_close = "Adj_Close"
    volume = "Volume"


    class TIMESERIES(Enum):
        DAILY = 'daily'
        WEEKLY = 'weekly'
        MONTHLY = 'monthly'




    @staticmethod
    def get_adj_close_key(ticker):
        key = "{}_{}".format(ticker, "Adj_Close")
        return key

    @staticmethod
    def get_high_key(ticker):
        key = "{}_{}".format(ticker, "High")
        return key

    @staticmethod
    def get_low_key(ticker):
        key = "{}_{}".format(ticker, "Low")
        return key

    @staticmethod
    def get_open_key(ticker):
        key = "{}_{}".format(ticker, "Open")
        return key

    @staticmethod
    def get_close_key(ticker):
        key = "{}_{}".format(ticker, "Close")
        return key

    @staticmethod
    def get_volume_key(ticker):
        key = "{}_{}".format(ticker, "Volume")
        return key

