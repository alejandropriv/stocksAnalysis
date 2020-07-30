from enum import Enum


class Constants:

    main_indicator_axis = "Template_indicator_axis"
    adj_close = "Adj_Close"
    volume = "Volume"

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


    #periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
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

    @staticmethod
    def get_daiy_ret_key(ticker):
        key = "{}_{}".format(ticker, "Daily_Ret")
        return key

    @staticmethod
    def get_key(ticker, base_key):
        key = "{}_{}".format(ticker, base_key)
        return key

