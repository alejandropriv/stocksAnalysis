from utilities.Constants import Constants
from kpi.KPI import KPI

from kpi.CAGR import CAGR

from kpi.Volatility import Volatility


class Sortino(KPI):
    kpi_name = Constants.get_key("Sortino")

    # RF is risk free rate
    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}

    def calculate(self, df, params=None):
        super().calculate(df, params)

        self.result = Sortino.get_sortino(df, self.params)
        return self.result

    @staticmethod
    def get_sortino(df, params=None):

        if params is None:
            params = {}

        if "rf" not in params.keys():
            # USA: risk free rate
            params = {"rf": 0.0144}

        rf = params["rf"]

        in_d = KPI.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        df = in_d[Constants.get_input_df_key()]

        d_result = {}


        for ticker in tickers:
            "function to calculate Sortino ratio ; rf is the risk free rate"

            cagr = CAGR.get_cagr(df[[ticker]], params)

            vol_params = {"negative": True}
            neg_vol = Volatility.get_volatility(df[[ticker]], vol_params)
            value = (cagr.result[ticker] - rf) / neg_vol.result[ticker]

            d_result[ticker] = value

        result = KPI.KPIResult(
            Sortino.kpi_name,
            d_result
        )

        return result
