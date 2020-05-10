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

        self.df_slope = df
        self.n = n
        self.ser = None

        self.plotter = plotter



    def set_input_data(self, df):

        super().set_input_data(df)


        # Set dataframe keys
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.slope_key = Constants.get_key(self.ticker, "SLOPE")
        self.ser = df[self.adj_close_key]

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

        print("Plotting SLOPE")
        if plotter is None:
            print("Please Select the main stock first.")
            raise IOError


        max_value = self.df_slope[self.slope_key].max()
        min_value = self.df_slope[self.slope_key].min()

        if plotter.ax_indicators is None or len(plotter.ax_indicators) <= 1:

            plotter.ax_indicators[self.slope_key] = plotter.ax_indicators[Constants.main_indicator_axis]
            #plotter.ax_indicators[Constants.main_indicator_axis]

        else:

            # instantiate a second axes that shares the same x-axis
            plotter.ax_indicators[self.slope_key] = \
                plotter.ax_indicators[Constants.main_indicator_axis].twinx()

        plotter.ax_indicators[self.slope_key].set_ylim(min_value - 1, max_value + 1)

        plotter.main_ax_indicator = plotter.ax_indicators[self.slope_key]
        plotter.ax_indicators[self.slope_key].tick_params(axis='y', labelcolor=color, size=20)
        plotter.plot_indicator(df=self.df_slope[[self.slope_key]], period=period, color=color)

        return plotter


