from utilities.Constants import Constants as Ct
from kpi.KPI import KPI

from kpi.CAGR import CAGR
from kpi.MaxDrawdown import MaxDrawdown
import pandas as pd


class Calmar(KPI):
    kpi_name = Ct.calmar_key()

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}

    def calculate(self, df, params=None):
        super().calculate(df, params)
        self.result = Calmar.get_calmar(df, self.params)
        return self.result

    @staticmethod
    def get_calmar(input_df, params=None):
        """function to calculate Calmar"""
        if params is None:
            params = {}

        cagr = CAGR.get_cagr(input_df, params)
        max_dd = MaxDrawdown.get_max_drawdown(input_df)

        result_df = pd.DataFrame()
        result_df[Calmar.kpi_name] = (cagr[Ct.cagr_key()]/max_dd[Ct.max_drawdown_key()])

        return result_df
