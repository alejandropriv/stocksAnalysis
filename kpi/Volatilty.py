from utilities.Constants import Constants
from kpi.KPI import KPI

import numpy as np




class Volatility(KPI):
    def __init__(self, df):
        super().__init__()

        self.adj_close_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)

        self.df = df.iloc[:, [self.adj_close_key]].copy()




    def calculate(self):
        "function to calculate annualized volatility of a trading strategy"
        self.df = self.df["Adj Close"].copy()
        self.df["daily_ret"] = self.df["Adj Close"].pct_change()
        vol = self.df["daily_ret"].std() * np.sqrt(252)
        return vol
