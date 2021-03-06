from kpi.KPI import KPI
from utilities.Constants import Constants as Ct

from kpi.CAGR import CAGR
from kpi.Volatility import Volatility
import pandas as pd



class Sharpe(KPI):
    kpi_name = Ct.sharpe_key()

    # rf = Risk free rate
    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}


    def calculate(self, df, params=None):
        super().calculate(df, params)
        self.result = Sharpe.get_sharpe(df, self.params)
        return self.result


    @staticmethod
    def get_sharpe(input_df, params):
        """ function to calculate sharpe """
        if params is None:
            params = {}

        if "rf" not in params.keys():
            # USA: risk free rate
            params["rf"] = 0.0144

        rf = params["rf"]

        "function to calculate sharpe ratio ; rf is the risk free rate"
        cagr = CAGR.get_cagr(input_df, params)
        volatility = Volatility.get_volatility(input_df, params)

        result_df = pd.DataFrame()
        result_df[Sharpe.kpi_name] = (cagr.loc[:, Ct.cagr_key()] - rf) / volatility.loc[:, Ct.volatility_key()]

        return result_df
