from utilities.Constants import Constants
from kpi.KPI import KPI
import pandas as pd


class MaxDrawdown(KPI):
    def __init__(self, df):
        super().__init__()

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_df(df)
        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:
            df_list.append(
                pd.concat(
                    [df[ticker].loc[:, [self.prices_key]], prices_temp],
                    axis=1,
                    keys=[ticker]
                )
            )

        df_kpi = pd.concat(
            df_list,
            axis=1
        )

        self.df = df_kpi.copy()


    def calculate(self):
        """ function to calculate max drawdown"        """

        super().calculate()

        df_result = []
        daily_ret_key = Constants.get_daiy_ret_key()
        cum_return_key = Constants.get_cum_return_key()
        cum_roll_max_key = Constants.get_key("cum_roll_max")
        drawdown_key = Constants.get_key("drawdown")
        drawdown_pct_key = Constants.get_key("drawdown_pct")

        value_key = Constants.get_key("MaxDrawdown")

        for ticker in self.tickers:
            df_data = self.df[ticker].copy()

            df_data = df_data[self.prices_key].pct_change()
            df_data[cum_return_key] = (1 + df_data[daily_ret_key]).cumprod()
            df_data[cum_roll_max_key] = df_data[cum_return_key].cummax()
            df_data[drawdown_key] = df_data[cum_roll_max_key] - df_data[cum_return_key]
            df_data[drawdown_pct_key] = df_data[drawdown_key] / df_data[cum_roll_max_key]
            max_dd = df_data[drawdown_pct_key].max()

            value = max_dd

            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return self.df
