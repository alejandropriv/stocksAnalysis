from kpi.KPI import KPI
from utilities.Constants import Constants


from kpi.CAGR import CAGR
from kpi.Volatility import Volatility
import pandas as pd



class Sharpe(KPI):

    # rf = Risk free rate
    def __init__(self, params=None):
        super().__init__(params)

    def calculate(self, df):
        self.result = Sharpe.get_max_drawdown(df, self.params)
        return self.result



    def get_sharpe(self, df, params):

        if params is None:
            params = {"rf": 0.05}

        if not params["period"]:
            params = {"period": "M"}

        rf = params["rf"]
        period = params["period"]

        in_d = KPI.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        df_result = []

        value_key = Constants.get_key("CAGR")


        for ticker in tickers:

            "function to calculate sharpe ratio ; rf is the risk free rate"
            cagr_obj = CAGR(params['period'])
            cagr = cagr_obj.calculate(df)

            volatility_obj = Volatility()
            volatility = volatility_obj.calculate()

            value = (cagr - rf)/volatility

            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)


        return self.df
