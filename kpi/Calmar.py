from utilities.Constants import Constants
from kpi.KPI import KPI

import numpy as np




class Calmar(KPI):
    def __init__(self, df, negative=False):
        super().__init__()

        self.adj_close_key = None
        self.negative = negative

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)

        self.df = df.iloc[:, [self.adj_close_key]].copy()




    def calculate(self):
        """function to calculate annualized volatility of a trading strategy"""
        daily_ret_key = Constants.get_daiy_ret_key(self.ticker)
        vol = None

        #Whole volatility was calculated
        if self.negative is False:
            self.df[daily_ret_key] = self.df[self.adj_close_key].pct_change()
            vol = self.df[daily_ret_key].std() * np.sqrt(252)

        else:
            self.df[daily_ret_key] = self.df[self.adj_close_key].pct_change()
            vol = self.df[self.df[daily_ret_key] < 0][daily_ret_key].std() * np.sqrt(252)

        return vol
