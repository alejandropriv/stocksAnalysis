import abc
from utilities.Constants import Constants



class Indicator(metaclass=abc.ABCMeta):


        @abc.abstractmethod
        def __init__(self):
            self.tickers = None
            self.df = None

        @abc.abstractmethod
        def set_input_data(self, df):
            if df is None:
                print("Error: data not found")
                raise IOError

            self.tickers = df.columns.levels[0]


        @abc.abstractmethod
        def calculate(self):
            """function to calculate the indicator"""
            if self.df is None:
                print("Error: DF has not been set Data not found to calculate the requested operation")
                raise IOError

