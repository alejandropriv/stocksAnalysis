import abc

from enum import Enum
import datetime
from utilities.Constants import Constants


class DataSource(metaclass=abc.ABCMeta):

    class DATASOURCETYPE(Enum):

        YFINANCE = 1
        PANDASDATAREADER = 2
        ALPHA = 3
        #YAHOOFINANCIALS = 4



    @abc.abstractmethod
    def __init__(self, tickers):

        if tickers is None:
            print("Tickers are None, please define your tickers")
            raise AttributeError

        self.tickers = tickers
        self.tickers_str = self.get_tickers_str()
        self.start_date = None
        self.end_date = None
        self.period = None
        self.interval = None
        self.interval_str = None

        self.daily_return = None


    def get_tickers_str(self):

        tickers_str = ""
        for ticker in self.tickers:
            tickers_str = tickers_str + " " + ticker

        return tickers_str

    @abc.abstractmethod
    def extract_historical_data(self,
                                start_date=datetime.date.today() - datetime.timedelta(365),
                                end_date=(datetime.date.today()),
                                period=None,
                                interval=Constants.INTERVAL.DAY):



        if end_date < start_date:
            print("End_Date must be bigger than Start_date")
            raise AttributeError

    @abc.abstractmethod
    def extract_data(self):
        pass





    # def get_statistical_data(self):
    #     # Handling NaN Values
    #     self.adj_close.fillna(method='bfill', axis=0,
    #                           inplace=True)  # Replaces NaN values with the next valid value along the column
    #
    #     self.adj_close.dropna(how='any', axis=0, inplace=True)  # Deletes any row where NaN value exists
    #
    #     # Mean, Median, Standard Deviation, daily return
    #     self.adj_close.mean()  # prints mean stock price for each stock
    #     self.adj_close.median()  # prints median stock price for each stock
    #     self.adj_close.std()  # prints standard deviation of stock price for each stock
    #
    #     self.daily_return = self.adj_close.pct_change()  # Creates dataframe with daily return for each stock
    #
    #     self.daily_return.mean()  # prints mean daily return for each stock
    #     self.daily_return.std()  # prints standard deviation of daily returns for each stock
    #
    #     # Rolling mean and standard deviation
    #     self.daily_return.rolling(window=20).mean()  # simple moving average
    #     self.daily_return.rolling(window=20).std()
    #
    #     self.daily_return.ewm(span=20, min_periods=20).mean()  # exponential moving average
    #     self.daily_return.ewm(span=20, min_periods=20).std()
