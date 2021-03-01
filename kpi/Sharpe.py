from kpi.KPI import KPI
from utilities.Constants import Constants


from kpi.CAGR import CAGR
from kpi.Volatility import Volatility
import pandas as pd



class Sharpe(KPI):

    kpi_name = "Sharpe"

    # rf = Risk free rate
    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}

    def calculate(self, df, params=None):
        super().calculate(df, params)

        self.result = Sharpe.get_sharpe(df, self.params)
        return self.result


    @staticmethod
    def get_sharpe(df, params):
        """ function to calculate sharpe """

        if params is None or "rf" not in params.keys():
            params = {"rf": 0.05}

        rf = params["rf"]

        in_d = KPI.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        df_result = []

        value_key = Constants.get_key("CAGR")


        for ticker in tickers:

            "function to calculate sharpe ratio ; rf is the risk free rate"
            cagr = CAGR.get_cagr(df[ticker][pricesk], [params['period']])

            volatility = Volatility.get_volatility(df[ticker][pricesk], [params['period']])

            value = (cagr - rf)/volatility

            df_result_value = pd.DataFrame([value], columns=[value_key])
            df_result.append(df_result_value.loc[:, [value_key]])

        result = KPI.KPIResult(
            Sharpe.kpi_name,
            pd.concat(df_result, axis=1, keys=tickers)
        )

        return result
