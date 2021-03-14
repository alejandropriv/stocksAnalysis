from enum import Enum


class Constants:

    adj_close = "Adj_Close"
    volume = "Volume"
    prices_axis = "prices_axis"
    volume_axis = "volume_axis"

    # intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    class INTERVAL(Enum):
        MINUTE = '1m'
        MINUTE2 = '2m'
        MINUTE5 = '5m'
        MINUTE15 = '15m'
        MINUTE30 = '30m'
        MINUTE60 = '60m'
        MINUTE90 = '90m'
        HOUR = '1h'
        DAY = '1d'
        DAY5 = '5d'
        WEEK = '1wk'
        MONTH = '1mo'
        MONTH3 = '3mo'


    # periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    class PERIOD(Enum):
        DAY = '1d'
        DAY5 = '5d'
        MONTH = '1mo'
        MONTH3 = '3mo'
        MONTH6 = '6mo'
        YEAR = '1y'
        YEAR2 = '2y'
        YEAR5 = '5y'
        YEAR10 = '10y'
        YTD = 'ytd'
        MAX = 'max'



    @staticmethod
    def get_prices_key():
        key = "{}".format("prices_key")
        return key\

    @staticmethod
    def get_tickers_key():
        key = "{}".format("tickers_key")
        return key

    @staticmethod
    def get_input_df_key():
        key = "{}".format("input_df_key")
        return key

    @staticmethod
    def get_adj_close_key():
        key = "{}".format("Adj_Close")
        return key

    @staticmethod
    def get_high_key():
        key = "{}".format("High")
        return key

    @staticmethod
    def get_low_key():
        key = "{}".format("Low")
        return key

    @staticmethod
    def get_open_key():
        key = "{}".format("Open")
        return key

    @staticmethod
    def get_close_key():
        key = "{}".format("Close")
        return key

    @staticmethod
    def get_volume_key():
        key = "{}".format("Volume")
        return key

    @staticmethod
    def get_ret_key():
        key = "{}".format("Ret")
        return key

    @staticmethod
    def get_cum_return_key():
        key = "{}".format("cum_return")
        return key

    @staticmethod
    def get_key(base_key):
        key = "{}".format(base_key)
        return key

