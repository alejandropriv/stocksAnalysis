from utilities.Constants import Constants
from kpi.KPI import KPI

from kpi.CAGR import CAGR
import pandas as pd

from kpi.Volatility import Volatility


class Sortino(KPI):

    #RF is risk free rate
    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}

    def calculate(self, df, params=None):
        super().calculate(df, params)

        self.result = Sortino.get_sortino(df, self.params)
        return self.result

    @staticmethod
    def get_sortino(self, df, params=None):

        if params is None or "rf" not in params.keys():
            params = {"rf": 0.05}

        rf = params["rf"]


        in_d = KPI.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        df_result = []

        value_key = Constants.get_key("CAGR")

        vol_params = {}
        for ticker in tickers:
            df_data = df[ticker][pricesk].copy()

            "function to calculate sharpe ratio ; rf is the risk free rate"
            cagr = CAGR.get_cagr(df_data, None)

            vol_params["negative"] = True
            neg_vol = Volatility.get_volatility(df, vol_params)

            value = (cagr - rf)/neg_vol

            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        df = pd.concat(df_result, axis=1, keys=self.tickers)

        return df
