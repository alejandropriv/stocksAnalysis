from utilities.Constants import Constants
from kpi.KPI import KPI

import numpy as np

from utilities.Handlers import Handlers



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
            params["negative"] = False

        reference_days = KPI.get_reference_days(params)

        negative = params["negative"]

        in_d = Handlers.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        d_result = {}

        daily_ret_key = Constants.get_ret_key()
        neg_daily_ret_key = Constants.get_key("neg_vol")


        for ticker in tickers:

            df[daily_ret_key] = df[ticker][pricesk].pct_change()

            # Whole volatility was calculated
            if negative is False:
                value = df[daily_ret_key].std() * np.sqrt(reference_days)

            else:
                df[neg_daily_ret_key] = np.where(df[daily_ret_key] < 0, df[daily_ret_key], 0)
                value = df[neg_daily_ret_key].std() * np.sqrt(reference_days)

            d_result[ticker] = value

        result = KPI.KPIResult(
            Volatility.kpi_name,
            d_result
        )

        return result
