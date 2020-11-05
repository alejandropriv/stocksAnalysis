import abc
import pandas as pd
from utilities.Constants import Constants



class Indicator(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def __init__(self):
        self.tickers = None
        self.df = None
        self.collapse = True
        self.prices_key = None

        # TODO: this is UI related, can this be removed from here? painless?
        self.in_main_plot = False

    @abc.abstractmethod
    def set_input_data(self, df):
        if df is None:
            raise ValueError("Error: data not found")

        df.columns = pd.MultiIndex.from_tuples(df.columns.values)

        self.tickers = df.columns.levels[0]

        # Set dataFrame keys
        adj_close_key = Constants.get_adj_close_key()
        close_key = Constants.get_close_key()

        if adj_close_key in df.columns is True:
            self.prices_key = adj_close_key

        else:
            self.prices_key = close_key


    @abc.abstractmethod
    def calculate(self):
        """function to calculate the indicator"""
        if self.df is None:
            print("Error: DF has not been set, there is no data to calculate the indicator. "
                  "Please verify the indicator constructor")
            raise IOError

