from utilities.Constants import Constants
from kpi.KPI import KPI

from kpi.CAGR import CAGR
import numpy as np

from kpi.Volatilty import Volatility



class Sortino(KPI):

    #RF is risk free rate
    def __init__(self, df, rf):
        super().__init__()

        self.adj_close_key = None
        self.rf = rf

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        self.df = df.copy()





    def calculate(self):
        super().calculate()

        "function to calculate sharpe ratio ; rf is the risk free rate"
        cagr_obj = CAGR(self.df)
        cagr = cagr_obj.calculate()

        volatility_obj = Volatility(self.df, negative=True)
        neg_vol = volatility_obj.calculate()

        sr = (cagr - self.rf)/neg_vol

        return sr
