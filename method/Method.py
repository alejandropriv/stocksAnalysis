from utilities.Constants import Constants
from kpi.KPI import KPI
import pandas as pd


class Method:
    def __init__(self, df=None):
        self.tickers = None
        self.df = None
        self.value = None
        self.prices_key = None
        self.name = None


    def set_input_df(self, df):
        if df is None:
            print("Error: data not found")
            raise IOError

        df.columns = pd.MultiIndex.from_tuples(df.columns.values)
        self.tickers = df.columns.levels[0]

        # Set dataFrame keys
        adj_close_key = Constants.get_adj_close_key()
        close_key = Constants.get_close_key()

        if adj_close_key in df.columns is True:
            self.prices_key = adj_close_key

        else:
            self.prices_key = close_key

        self.value = None


    def backtest(self):
        pass
