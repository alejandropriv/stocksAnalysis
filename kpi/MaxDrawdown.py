from utilities.Constants import Constants
from kpi.KPI import KPI
import pandas as pd
from utilities.Handlers import Handlers



class MaxDrawdown(KPI):
    kpi_name = Constants.max_drawdown_key()

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}

    def calculate(self, df, params=None):
        super().calculate(df)

        self.result = MaxDrawdown.get_max_drawdown(df)
        return self.result

    @staticmethod
    def get_max_drawdown(input_df):
        """ function to calculate max drawdown"        """

        df = input_df.copy()
        df.columns = df.columns.droplevel(1)

        cumprod_df = (1 + df).cumprod()
        cum_roll_max_df = cumprod_df.cummax()
        drawdown_df = cum_roll_max_df - cumprod_df
        drawdown_pct_df = drawdown_df / cum_roll_max_df
        result_df = pd.DataFrame()
        result_df[MaxDrawdown.kpi_name] = drawdown_pct_df.max()

        return result_df
