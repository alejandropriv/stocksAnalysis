from utilities.Constants import Constants
from kpi.KPI import KPI

from kpi.CAGR import CAGR
from kpi.MaxDrawdown import MaxDrawdown
from utilities.Handlers import Handlers


class Calmar(KPI):
    kpi_name = Constants.get_key("Calmar")

    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}

    def calculate(self, df, params=None):
        super().calculate(df, params)
        self.result = Calmar.get_calmar(df, self.params)
        return self.result

    @staticmethod
    def get_calmar(df, params=None):
        """function to calculate Calmar"""

        if params is None:
            params = {}

        in_d = Handlers.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        df = in_d[Constants.get_input_df_key()]

        d_result = {}

        for ticker in tickers:
            cagr = CAGR.get_cagr(df[[ticker]], params)
            max_dd = MaxDrawdown.get_max_drawdown(df[[ticker]], params)
            value = cagr.result[ticker] / max_dd.result[ticker]

            d_result[ticker] = value

        result = KPI.KPIResult(
            Calmar.kpi_name,
            d_result
        )

        return result
