from utilities.Constants import Constants
from kpi.KPI import KPI
import pandas as pd




class CAGR(KPI):
    def __init__(self, df):
        super().__init__()

        self.close_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:
            df_list.append(
                pd.concat(
                    [df[ticker].loc[:, [self.prices_key]], prices_temp],
                    axis=1,
                    keys=[ticker]
                )
            )

        df_kpi = pd.concat(
            df_list,
            axis=1
        )

        self.df = df_kpi.copy()





    def calculate(self):
        """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""
        super().calculate()

        df_result = []

        for ticker in self.tickers:

            df_data = self.df[ticker].copy()

            daily_ret_key = Constants.get_daiy_ret_key(self.ticker)
            cum_ret_key = Constants.get_key(self.ticker, "cum_return")

            self.df[daily_ret_key] = self.df[self.adj_close_key].pct_change()
            self.df[cum_ret_key] = (1 + self.df[daily_ret_key]).cumprod()
            n = len(self.df) / 252
            self.value = (self.df[cum_ret_key][-1]) ** (1 / n) - 1
            return self.value

