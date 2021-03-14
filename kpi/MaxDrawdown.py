from utilities.Constants import Constants
from kpi.KPI import KPI
import pandas as pd
from utilities.Handlers import Handlers



class MaxDrawdown(KPI):
    kpi_name = Constants.get_key("MaxDrawdown")

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}

    def calculate(self, df, params=None):
        super().calculate(df, params)

        self.result = MaxDrawdown.get_max_drawdown(df, self.params)
        return self.result

    @staticmethod
    def get_max_drawdown(df, params):

        if params is None:
            params = {}

        """ function to calculate max drawdown"        """
        in_d = Handlers.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        d_result = {}
        daily_ret_key = Constants.get_ret_key()
        cum_return_key = Constants.get_cum_return_key()
        cum_roll_max_key = Constants.get_key("cum_roll_max")
        drawdown_key = Constants.get_key("drawdown")
        drawdown_pct_key = Constants.get_key("drawdown_pct")

        df_data = pd.DataFrame()


        for ticker in tickers:

            df_data[daily_ret_key] = df[ticker][pricesk].pct_change()
            df_data[cum_return_key] = (1 + df_data[daily_ret_key]).cumprod()
            df_data[cum_roll_max_key] = df_data[cum_return_key].cummax()
            df_data[drawdown_key] = df_data[cum_roll_max_key] - df_data[cum_return_key]
            df_data[drawdown_pct_key] = df_data[drawdown_key] / df_data[cum_roll_max_key]
            value = df_data[drawdown_pct_key].max()

            d_result[ticker] = value

        result = KPI.KPIResult(
            MaxDrawdown.kpi_name,
            d_result
        )

        return result
