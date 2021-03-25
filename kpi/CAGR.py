from utilities.Constants import Constants as Ct
from kpi.KPI import KPI
import pandas as pd


class CAGR(KPI):
    kpi_name = Ct.cagr_key()

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}


    def calculate(self, df, params=None):
        """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""

        super().calculate(df, params)

        self.result = CAGR.get_cagr(df, self.params)
        return self.result

    # Params: {period:Ct.INTERVAL.MONTH|Ct.INTERVAL.DAY}
    # DF should be a percentage change
    @staticmethod
    def get_cagr(input_df, params=None):
        """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""

        reference_days = KPI.get_reference_days(params)
        df = input_df.copy()
        df.columns = df.columns.droplevel(1)


        cagr_data = (1 + df).cumprod()
        n = len(cagr_data) / reference_days
        result_df = ((cagr_data[-1:]) ** (1 / n) - 1).reset_index(drop=True)


        result_df.columns = pd.MultiIndex.from_product([result_df.columns, [CAGR.kpi_name]])

        return result_df
