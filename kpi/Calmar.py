from utilities.Constants import Constants
from kpi.KPI import KPI
import pandas as pd


import numpy as np


class Calmar(KPI):
    def __init__(self, df=None):
        super().__init__()

        self.negative = False

        if df is not None:
            self.set_input_df(df)


    def set_input_data(self, df, negative=False):
        self.set_input_df(df)

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


        self.negative = negative

    def calculate(self):
        """function to calculate Calmar"""
        super().calculate()


        df_result = []
        daily_ret_key = Constants.get_daiy_ret_key()
        value_key = Constants.get_key("Calmar")


        for ticker in self.tickers:
            df_data = self.df[ticker].copy()

            #Whole volatility was calculated
            if self.negative is False:
                df_data[daily_ret_key] = df_data[self.prices_key].pct_change()
                value = df_data[daily_ret_key].std() * np.sqrt(252)

            else:
                df_data[daily_ret_key] = df_data[self.prices_key].pct_change()
                value = df_data[self.df[daily_ret_key] < 0][daily_ret_key].std() * np.sqrt(252)

            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return self.df
