from utilities.Constants import Constants
from kpi.KPI import KPI

from kpi.CAGR import CAGR
import pandas as pd

from kpi.Volatilty import Volatility


class Sortino(KPI):

    #RF is risk free rate
    def __init__(self, df=None, rf=None):
        super().__init__()

        self.adj_close_key = None
        self.rf = rf

        if df is not None:
            self.set_input_df(df)


    def set_input_data(self, df, rf):
        self.set_input_df(df)

        self.rf = rf

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

        super().calculate()

        df_result = []

        value_key = Constants.get_key("CAGR")


        for ticker in self.tickers:
            df_data = self.df[ticker].copy()

            "function to calculate sharpe ratio ; rf is the risk free rate"
            cagr_obj = CAGR(df_data)
            cagr = cagr_obj.calculate()

            volatility_obj = Volatility(self.df, negative=True)
            neg_vol = volatility_obj.calculate()

            value = (cagr - self.rf)/neg_vol

            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return self.df
