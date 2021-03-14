from utilities.Constants import Constants
from kpi.KPI import KPI
import pandas as pd
from utilities.Handlers import Handlers


class CAGR(KPI):
    kpi_name = Constants.get_key("CAGR")

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}


    def calculate(self, df, params=None):
        """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""

        super().calculate(df, params)

        self.result = CAGR.get_cagr(df, self.params)
        return self.result


    @staticmethod
    def get_cagr(df, params=None):
        """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""

        if params is None:
            params = {}

        reference_days = KPI.get_reference_days(params)

        in_d = Handlers.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        d_result = {}
        ret_key = Constants.get_ret_key()
        cum_ret_key = Constants.get_cum_return_key()
        df_data = pd.DataFrame()

        for ticker in tickers:

            df_data[ret_key] = df[ticker][pricesk].pct_change()
            df_data[cum_ret_key] = (1 + df_data[ret_key]).cumprod()
            n = len(df.index) / reference_days
            value = (df_data[cum_ret_key][-1]) ** (1 / n) - 1

            d_result[ticker] = value

        result = KPI.KPIResult(
            CAGR.kpi_name,
            d_result
        )

        return result


    def calculate_with_daily_return(self):
        pass

    def calculate_with_monthly_return(self):
        pass