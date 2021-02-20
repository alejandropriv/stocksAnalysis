from utilities.Constants import Constants
from kpi.KPI import KPI
import pandas as pd


class CAGR(KPI):
    def __init__(self, df=None):
        super().__init__()

        if df is not None:
            self.set_input_data(df)

    def set_input_data(self, df):
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


    def calculate(self):
        """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""
        super().calculate()

        df_result = []
        daily_ret_key = Constants.get_daiy_ret_key()
        cum_ret_key = Constants.get_cum_return_key()
        value_key = Constants.get_key("CAGR")

        for ticker in self.tickers:
            df_data = self.df[ticker].copy()

            df_data[daily_ret_key] = df_data[self.prices_key].pct_change()
            df_data[cum_ret_key] = (1 + df_data[daily_ret_key]).cumprod()
            n = len(self.df.index) / 252
            value = (df_data[cum_ret_key][-1]) ** (1 / n) - 1

            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return self.df
