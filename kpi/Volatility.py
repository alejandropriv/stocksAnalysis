from utilities.Constants import Constants
from kpi.KPI import KPI

import numpy as np


class Volatility(KPI):

    kpi_name = Constants.get_key("Volatility")

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}


    def calculate(self, df, params=None):
        super().calculate(df, params)

        self.result = Volatility.get_volatility(df, self.params)
        return self.result


    @staticmethod
    def get_volatility(df, params=None):
        """function to calculate annualized volatility of a trading strategy"""

        if params is None:
            params = {}

        if "negative" not in params.keys():
            params = {"negative": False}

        negative = params["negative"]

        in_d = KPI.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        d_result = {}

        daily_ret_key = Constants.get_day_ret_key()
        neg_daily_ret_key = Constants.get_key("neg_vol")


        for ticker in tickers:

            # Whole volatility was calculated
            if negative is False:
                df[daily_ret_key] = df[ticker][pricesk].pct_change()
                value = df[daily_ret_key].std() * np.sqrt(252)

            else:
                df[daily_ret_key] = df[ticker][pricesk].pct_change()
                df[neg_daily_ret_key] = np.where(df[daily_ret_key] < 0, df[daily_ret_key], 0)
                value = df[neg_daily_ret_key].std() * np.sqrt(252)

            d_result[ticker] = value

        result = KPI.KPIResult(
            Volatility.kpi_name,
            d_result
        )

        return result
