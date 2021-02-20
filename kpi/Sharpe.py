from kpi.KPI import KPI
from utilities.Constants import Constants


from kpi.CAGR import CAGR
from kpi.Volatilty import Volatility
import pandas as pd



class Sharpe(KPI):

    # rf = Risk free rate
    def __init__(self, df, rf=None):
        super().__init__()

        self.rf = None

        if df is not None:
            self.set_input_data(df, rf)


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

            volatility_obj = Volatility(self.df)
            volatility = volatility_obj.calculate()

            value = (cagr - self.rf)/volatility

            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)


        return self.df
