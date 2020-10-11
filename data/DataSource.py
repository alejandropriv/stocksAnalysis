import abc

from enum import Enum
import datetime
from utilities.Constants import Constants


class DATASOURCETYPE(Enum):
    YFINANCE = 1
    PANDASDATAREADER = 2
    ALPHA = 3


class DataSource(metaclass=abc.ABCMeta):


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
        self.time_delta = None
        self.interval = None
        self.interval_str = None

        self.daily_return = None


    def validate_dates(self):

        if self.end_date is None:
            print("Error: end_date is None, Set a valid end date.")
            return False

        if self.period is None and self.start_date is None:
            print("Error: Please set start_date or period")
            return False


        if self.period is None:
            self.period = "max"
        else:
            self.start_date = None
            self.end_date = None


        if self.start_date is not None:
            if self.start_date > self.end_date:

                print("Error:  Start_date should be earlier than end date")
                return False


        elif self.time_delta is not None and self.time_delta > 0:
            self.start_date = datetime.datetime.today() - datetime.timedelta(self.time_delta)


        else:
            print("Error: Neither the Start_date nor the time_delta were defined ")
            return False

        return True





    def get_tickers_str(self):

        tickers_str = ""
        for ticker in self.tickers:
            tickers_str = tickers_str + " " + ticker

        return tickers_str

    @abc.abstractmethod
    def extract_historical_data(self,
                                start_date=None,
                                end_date=(datetime.date.today()),
                                time_delta=None,
                                period=None,
                                interval=Constants.INTERVAL.DAY):

        self.start_date = start_date
        self.end_date = end_date
        self.time_delta = time_delta
        self.period = period
        self.interval = interval
        self.interval_str = interval.name






    @abc.abstractmethod
    def get_prices(self, tickers, key_titles):
        pass

    @abc.abstractmethod
    def extract_fundamentals(self, tickers, required_elements):
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
