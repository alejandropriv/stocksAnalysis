from enum import Enum


class Constants:

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
    def prices_key():
        key = "{}".format("prices_key")
        return key\

    @staticmethod
    def tickers_key():
        key = "{}".format("tickers")
        return key

    @staticmethod
    def input_df_key():
        key = "{}".format("input_df_key")
        return key

    @staticmethod
    def adj_close_key():
        key = "{}".format("Adj Close")
        return key

    @staticmethod
    def high_key():
        key = "{}".format("High")
        return key

    @staticmethod
    def low_key():
        key = "{}".format("Low")
        return key

    @staticmethod
    def open_key():
        key = "{}".format("Open")
        return key

    @staticmethod
    def close_key():
        key = "{}".format("Close")
        return key

    @staticmethod
    def volume_key():
        key = "{}".format("Volume")
        return key

    @staticmethod
    def ret_key():
        key = "{}".format("Ret")
        return key

    @staticmethod
    def start_date_key():
        key = "{}".format("start_date")
        return key

    @staticmethod
    def end_date_key():
        key = "{}".format("end_date")
        return key

    @staticmethod
    def cum_return_key():
        key = "{}".format("cum_return")
        return key

    @staticmethod
    def historical_type_key():
        key = "{}".format("has_historical_data")
        return key

    @staticmethod
    def period_key():
        key = "{}".format("period")
        return key

    @staticmethod
    def interval_key():
        key = "{}".format("interval")
        return key

    @staticmethod
    def fundamentals_type_key():
        key = "{}".format("has_fundamentals_data")
        return key

    @staticmethod
    def indicators_key():
        key = "{}".format("indicators")
        return key

    @staticmethod
    def bulk_key():
        key = "{}".format("bulk")
        return key

    @staticmethod
    def fundamentals_options_key():
        key = "{}".format("fundamentals_options")
        return key

    @staticmethod
    def force_fundamentals_key():
        key = "{}".format("force_fundamentals")
        return key

    # KPIS keys
    @staticmethod
    def cagr_key():
        key = "{}".format("cagr")
        return key

    @staticmethod
    def calmar_key():
        key = "{}".format("calmar")
        return key

    @staticmethod
    def max_drawdown_key():
        key = "{}".format("max_drawdown")
        return key

    @staticmethod
    def volatility_key():
        key = "{}".format("volatility")
        return key

    @staticmethod
    def neg_volatility_key():
        key = "{}".format("volatility")
        return key


    @staticmethod
    def sharpe_key():
        key = "{}".format("sharpe")
        return key

    @staticmethod
    def sortino_key():
        key = "{}".format("sortino")
        return key


    @staticmethod
    def get_key(base_key):
        key = "{}".format(base_key)
        return key

