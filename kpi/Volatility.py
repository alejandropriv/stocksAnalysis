from utilities.Constants import Constants
from kpi.KPI import KPI

import numpy as np
import pandas as pd




class Volatility(KPI):

    kpi_name = "Volatility"

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}


    def calculate(self, df, params=None):
        super().calculate(df, params)

        self.result = Volatility.get_volatility(df, self.params)
        return self.result


    @staticmethod
    def get_volatility(df, params):
        """function to calculate annualized volatility of a trading strategy"""

        if params is None or "negative" not in params.keys():
            params = {"negative": False}

        negative = params["negative"]

        in_d = KPI.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        df_result = []

        value_key = Constants.get_key("CAGR")
        daily_ret_key = Constants.get_daiy_ret_key()

        for ticker in tickers:

            # Whole volatility was calculated
            if negative is False:
                df[daily_ret_key] = df[ticker][pricesk].pct_change()
                value = df[daily_ret_key].std() * np.sqrt(252)

            else:
                df[daily_ret_key] = df[ticker][pricesk].pct_change()
                value = df[df[daily_ret_key] < 0][daily_ret_key].std() * np.sqrt(252)


            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return self.df
