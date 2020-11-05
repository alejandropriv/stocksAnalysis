import abc
import pandas as pd

class ValueInvestmentMetric(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def __init__(self):
        self.tickers = None
        self.fundamentals_df = None
        self.metric_df = pd.DataFrame()


    @abc.abstractmethod
    def set_input_data(self, fundamentals):
        if fundamentals is None:
            raise ValueError("Error: data not found")

        self.tickers = fundamentals.tickers

    @abc.abstractmethod
    def calculate(self):
        """function to calculate the indicator"""
        if self.fundamentals_df is None:
            print("Error: DF has not been set, there is no data to calculate the indicator. "
                  "Please verify the indicator constructor")
            raise IOError

