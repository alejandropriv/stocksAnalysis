from utilities.Constants import Constants
from kpi.KPI import KPI
import pandas as pd


import numpy as np


class Calmar(KPI):

    kpi_name = "Calmar"

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}


    def calculate(self, df, params=None):
        super().calculate(df, params)

        self.result = Calmar.get_calmar(df, self.params)
        return self.result

    @staticmethod
    def get_calmar(df, params=None):
        """function to calculate Calmar"""

        if params is None or "negative" not in params.keys():
            params = {"negative": False}

        elif params["negative"] != True:
            params["negative"] = False

        negative = params["negative"]

        in_d = KPI.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        df_result = []
        daily_ret_key = Constants.get_daiy_ret_key()
        value_key = Constants.get_key(Calmar.kpi_name)
        df_data = pd.DataFrame()



        for ticker in tickers:

            #Whole volatility was calculated
            if negative is False:
                df_data[daily_ret_key] = df[ticker][pricesk].pct_change()
                value = df_data[daily_ret_key].std() * np.sqrt(252)

            else:
                df_data[daily_ret_key] = df[ticker][pricesk].pct_change()
                value = \
                    df_data[df_data[daily_ret_key] < 0][daily_ret_key].std() * np.sqrt(252)

            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        result = KPI.KPIResult(
            Calmar.kpi_name,
            pd.concat(df_result, axis=1, keys=tickers)
        )

        return result
