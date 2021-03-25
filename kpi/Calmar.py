from utilities.Constants import Constants
from kpi.KPI import KPI

from kpi.CAGR import CAGR
from kpi.MaxDrawdown import MaxDrawdown
import pandas as pd


class Calmar(KPI):
    kpi_name = Constants.calmar_key()

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

        cagr.columns = cagr.columns.droplevel(1)
        max_dd.columns = max_dd.columns.droplevel(1)

        result_df = cagr / max_dd
        result_df.columns = pd.MultiIndex.from_product([result_df.columns, [Calmar.kpi_name]])

        return result_df
