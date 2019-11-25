import abc

from enum import Enum

import datetime



class HistoricalData(metaclass=abc.ABCMeta):

    class DATASOURCETYPE(Enum):

        YAHOOFINANCIALS = 1
        YAHOOAPI = 2
        ALPHAAPI = 3


    class TIMESERIES(Enum):
        DAILY = 'daily'
        WEEKLY = 'weekly'
        MONTHLY = 'monthly'



    tickers = None
    start_date = None
    end_date = None
    time_series = None
    data_columns = None

    adj_close = None
    daily_return = None



    @abc.abstractmethod
    def __init__(self):
        pass


    @abc.abstractmethod
    def extract_historical_data(self,
                                tickers,
                                start_date,
                                end_date,
                                time_series,
                                data_columns):
        pass

    @abc.abstractmethod
    def extract_data(self):
        pass


    def get_statistical_data(self):
        # Handling NaN Values
        self.adj_close.fillna(method='bfill', axis=0,
                              inplace=True)  # Replaces NaN values with the next valid value along the column

        self.adj_close.dropna(how='any', axis=0, inplace=True)  # Deletes any row where NaN value exists

        # Mean, Median, Standard Deviation, daily return
        self.adj_close.mean()  # prints mean stock price for each stock
        self.adj_close.median()  # prints median stock price for each stock
        self.adj_close.std()  # prints standard deviation of stock price for each stock

        self.daily_return = self.adj_close.pct_change()  # Creates dataframe with daily return for each stock

        self.daily_return.mean()  # prints mean daily return for each stock
        self.daily_return.std()  # prints standard deviation of daily returns for each stock

        # Rolling mean and standard deviation
        self.daily_return.rolling(window=20).mean()  # simple moving average
        self.daily_return.rolling(window=20).std()

        self.daily_return.ewm(span=20, min_periods=20).mean()  # exponential moving average
        self.daily_return.ewm(span=20, min_periods=20).std()


