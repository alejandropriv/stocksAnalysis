from utilities.Constants import Constants
from kpi.KPI import KPI

import numpy as np




class MaxDrawdown(KPI):
    def __init__(self, df, negative=False):
        super().__init__()

        self.adj_close_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)

        self.df = df.iloc[:, [self.adj_close_key]].copy()




    def calculate(self):
        super().calculate()

        "function to calculate max drawdown"
        daily_ret_key = Constants.get_daiy_ret_key(self.ticker)
        cum_return_key = Constants.get_key(self.ticker, "cum_return")
        cum_roll_max_key = Constants.get_key(self.ticker, "cum_roll_max")
        drawdown_key = Constants.get_key(self.ticker, "drawdown")
        drawdown_pct_key = Constants.get_key(self.ticker, "drawdown_pct")

        self.df[daily_ret_key] = self.df[self.adj_close_key].pct_change()
        self.df[cum_return_key] = (1 + self.df[daily_ret_key]).cumprod()
        self.df[cum_roll_max_key] = self.df[cum_return_key].cummax()
        self.df[drawdown_key] = self.df[cum_roll_max_key] - self.df[cum_return_key]
        self.df[drawdown_pct_key] = self.df[drawdown_key] / self.df[cum_roll_max_key]
        max_dd = self.df[drawdown_pct_key].max()
        self.value = max_dd
        return self.value
