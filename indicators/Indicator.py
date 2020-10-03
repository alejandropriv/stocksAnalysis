import abc
import pandas as pd


class Indicator(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def __init__(self):
        self.tickers = None
        self.df = None
        self.collapse = True
        self.in_main_plot = False

    @abc.abstractmethod
    def set_input_data(self, df):
        if df is None:
            print("Error: data not found")
            raise IOError

        df.columns = pd.MultiIndex.from_tuples(df.columns.values)

        self.tickers = df.columns.levels[0]

    @abc.abstractmethod
    def calculate(self):
        """function to calculate the indicator"""
        if self.df is None:
            print("Error: DF has not been set Data not found to calculate the requested operation")
            raise IOError

