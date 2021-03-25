from utilities.Constants import Constants as Ct
from kpi.KPI import KPI

from kpi.CAGR import CAGR

from kpi.Volatility import Volatility
import pandas as pd




class Sortino(KPI):
    kpi_name = Ct.sortino_key()

    # RF is risk free rate
    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}

    def calculate(self, df, params=None):
        super().calculate(df, params)

        self.result = Sortino.get_sortino(df, self.params)
        return self.result

    @staticmethod
    def get_sortino(input_df, params=None):

        if params is None:
            params = {}

        if "rf" not in params.keys():
            # USA: risk free rate
            params = {"rf": 0.0144}

        rf = params["rf"]

        "function to calculate Sortino ratio ; rf is the risk free rate"

        cagr = CAGR.get_cagr(input_df, params)

        vol_params = params
        vol_params[Ct.neg_volatility_key()] = True
        neg_vol = Volatility.get_volatility(input_df, vol_params)

        cagr.columns = cagr.columns.droplevel(1)
        neg_vol.columns = neg_vol.columns.droplevel(1)

        result_df = (cagr - rf) / neg_vol

        result_df.columns = pd.MultiIndex.from_product([result_df.columns, [Sortino.kpi_name]])

        return result_df
