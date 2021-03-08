from kpi.KPI import KPI
from utilities.Constants import Constants

from kpi.CAGR import CAGR
from kpi.Volatility import Volatility


class Sharpe(KPI):
    kpi_name = Constants.get_key("Sharpe")

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
            # USA: risk free rate
            params = {"rf": 0.0144}


        rf = params["rf"]

        in_d = KPI.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        df = in_d[Constants.get_input_df_key()]

        d_result = {}

        for ticker in tickers:
            "function to calculate sharpe ratio ; rf is the risk free rate"
            cagr = CAGR.get_cagr(df[[ticker]], params)  # TODO: Fix here dataframe double index

            volatility = Volatility.get_volatility(df[[ticker]], params)

            value = (cagr.result[ticker] - rf) / volatility.result[ticker]

            d_result[ticker] = value

        result = KPI.KPIResult(
            Sharpe.kpi_name,
            d_result
        )

        return result
