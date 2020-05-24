from utilities.Constants import Constants
from indicators.Indicator import Indicator
import pandas as pd


import numpy as np

import statsmodels.api as sm


class Slope(Indicator):

    # price is Dataframe
    # n number of consecutive points to calculate the slope
    def __init__(self, df=None, n=5, plotter=None):

        super().__init__()

        self.n = n
        self.ser = None

        self.plotter = plotter

        self.adj_close_key = None
        self.slope_key = None


    def set_input_data(self, df):

        super().set_input_data(df)


        # Set dataframe keys
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.slope_key = Constants.get_key(self.ticker, "SLOPE")
        self.ser = df[self.adj_close_key]
        self.ser.ticker = self.ticker

    def calculate(self):
        "function to calculate the slope of n consecutive points on a plot"
        slopes = [i * 0 for i in range(self.n - 1)]
        for i in range(self.n, len(self.ser) + 1):
            y = self.ser[i - self.n:i]
            x = np.array(range(self.    n))
            y_scaled = (y - y.min()) / (y.max() - y.min())
            x_scaled = (x - x.min()) / (x.max() - x.min())
            x_scaled = sm.add_constant(x_scaled)
            model = sm.OLS(y_scaled, x_scaled)
            results = model.fit()
            slopes.append(results.params[-1])

        slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))

        self.df_slope = pd.DataFrame()
        self.df_slope[self.slope_key] = np.array(slope_angle)
        #return np.array(slope_angle)


    # expect Stock, volume, Indicator
    def plot(self, plotter=None, period=100, color="tab:green"):

        super().plot(plotter=plotter, period=period, color=color)

        self.plot_indicator(
            plotter=plotter,
            period=period,
            key=self.obv_key,
            color=color,
            legend_position=None
        )
