from utilities.Constants import Constants as Ct
from kpi.KPI import KPI
import pandas as pd
import numpy as np


class Volatility(KPI):

    kpi_name = Ct.volatility_key()

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}


    def calculate(self, df, params=None):
        super().calculate(df, params)

        self.result = Volatility.get_volatility(df, self.params)
        return self.result


    @staticmethod
    def get_volatility(input_df, params=None):
        """function to calculate annualized volatility of a trading strategy"""

        if params is None:
            raise ValueError("Please set the corresponding Interval parameter"
                             "{interval:Ct.INTERVAL.MONTH|Ct.INTERVAL.DAY}")

        if Ct.neg_volatility_key() not in params.keys():
            params[Ct.neg_volatility_key()] = False


        reference_days = KPI.get_reference_days(params)
        negative = params[Ct.neg_volatility_key()]

        df = input_df.copy()

        df.columns = df.columns.droplevel(1)

        result_df = pd.DataFrame()
        # Whole volatility was calculated
        if negative is False:
            result_df[Volatility.kpi_name] = (df.std() * np.sqrt(reference_days))

        else:
            df_neg = df.where(df < 0, 0)
            result_df[Volatility.kpi_name] = (df_neg.std() * np.sqrt(reference_days))

        return result_df
