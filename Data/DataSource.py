import abc
from enum import Enum

class DataSource(metaclass=abc.ABCMeta):

    class DataSourceType(Enum):

        YAHOOFINANCIALS = 1
        YAHOOAPI = 2
        ALPHAAPI = 3


    class TimeInterval(Enum):
        DAILY = 'daily'
        WEEKLY = 'weekly'
        MONTHLY = 'monthly'


    ticker = None
    start_date = None
    end_date = None

    @abc.abstractmethod
    def __init__(self, ticker, start_date, end_date):
        print("This constructor needs to be implemented in the child class")
        pass

    @abc.abstractmethod
    def __init__(self, ticker, start_date, end_date):
        pass


    @abc.abstractmethod
    def extract_historical_data(self):
        pass


    @abc.abstractmethod
    def extract_data(self):
        pass


