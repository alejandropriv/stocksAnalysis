import abc

from enum import Enum
import datetime
from utilities.Constants import Constants


class DATASOURCETYPE(Enum):
    YFINANCE = 1
    PANDASDATAREADER = 2
    ALPHA = 3


class DataSource(metaclass=abc.ABCMeta):


    def __init__(self):
        pass




    @staticmethod
    def validate_dates(dates=None):

        if dates is None:
            raise ValueError("Wrong input parameters, Verify your code!!!")

        if dates["end_date"] is None:
            raise ValueError("Error: end_date is None, Set a valid end date.")

        if dates["period"] is None and dates["start_date"] is None:
            raise ValueError("Error: Please set start_date or period")


        if dates["period"] is None:
            dates["period"] = "max"
        else:
            dates["start_date"] = None
            dates["end_date"] = None


        if dates["start_date"] is not None:
            if dates["start_date"] > dates["end_date"]:
                raise ValueError("Error:  Start_date should be earlier than end date")


        elif dates["time_delta"] is not None and dates["time_delta"]  > 0:
            dates["start_date"] = datetime.datetime.today() - datetime.timedelta(dates["time_delta"] )


        else:
            raise ValueError("Error: Neither the Start_date nor the time_delta were defined ")

        return True





    @staticmethod
    def get_tickers_str(tickers):

        tickers_str = ""
        for ticker in tickers:
            tickers_str = tickers_str + " " + ticker

        return tickers_str

    @abc.abstractmethod
    def extract_historical_data(self,
                                tickers=None,
                                start_date=None,
                                end_date=(datetime.date.today()),
                                period=None,
                                interval=Constants.INTERVAL.DAY,
                                time_delta=None,
                                ):

        if tickers is None:
            print("Tickers are None, please define your tickers")
            raise AttributeError



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
