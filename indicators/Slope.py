from utilities.Constants import Constants
from indicators.Indicator import Indicator
import pandas as pd


import numpy as np

import statsmodels.api as sm


class Slope(Indicator):

    # price is Dataframe
    # n number of consecutive points to calculate the slope
    def __init__(self, df=None, n=5):

        super().__init__()


        self.n = n
        self.ser = None

        self.prices_key = None
        self.indicator_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):

        super().set_input_data(df)

        # Set dataframe keys
        self.indicator_key = Constants.get_key("SLOPE")

        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:
            self.ser[ticker] = df[ticker][self.prices_key]

            df_list.append(
                pd.concat(
                    [df[ticker].loc[:, [self.prices_key]], prices_temp],
                    axis=1,
                    keys=[ticker]
                )
            )

        df_indicator = pd.concat(
            df_list,
            axis=1
        )

        self.df = df_indicator.copy()

    def calculate(self):
        """function to calculate the slope of n consecutive points on a plot"""
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

        # self.df = pd.DataFrame()
        self.df[self.slope_key] = np.array(slope_angle) # +300
        # return np.array(slope_angle)


    # expect Stock, volume, Indicator
    def plot(self, plotter=None, period=100, color="tab:green"):

        super().plot(plotter=plotter, period=period, color=color)

        self.plot_indicator(
            plotter=plotter,
            period=period,
            key=self.slope_key,
            color=color,
            legend_position=None
        )
        # super().plot(plotter=plotter, period=period, color=color)
        #
        # x = self.df.iloc[:, [0]]
        # index = x.iloc[-period:, :].index
        #
        # # put period for the data also
        # df = self.df.iloc[-period:, :]
        #
        # if plotter.ax_main is None:
        #     print("Error: Main Stock has not been plotted, "
        #           "plot a stock and then plot the associated bollinger bands")
        #     raise IOError
        #
        # plotter.ax_main[Constants.adj_close].plot(index, df[self.slope_key]+250, color=color)
