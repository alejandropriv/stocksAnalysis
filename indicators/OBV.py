from utilities.Constants import Constants
import numpy as np


class OBV:
    #TODO verify the correct data is present
    # df requires:  price adjusted close
    #               volume
    def __init__(self, df=None, n=14, plotter=None):

        if df is None:
            print("Error: data not found")
            raise IOError


        self.ticker = df.ticker

        # Set dataframe keys
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.volume_key = Constants.get_volume_key(self.ticker)
        self.obv_key = Constants.get_key(self.ticker, "OBV")

        keys = [self.adj_close_key, self.volume_key]
        for key in keys:
            if key not in df.columns:
                print("Error: df is missing {} data".format(key))
                raise IOError


        self.n = n
        self.df_obv = df[[self.adj_close_key]].copy()
        self.df_obv[self.volume_key] = df[[self.volume_key]]
        self.df_obv.ticker = df.ticker

        self.plotter = plotter

    def calculate(self):
        """function to calculate On Balance Volume"""

        daily_ret_key = Constants.get_key(self.ticker, "daily_ret")
        direction_key = Constants.get_key(self.ticker, "direction")
        volume_adjusted_key = Constants.get_key(self.ticker, "vol_adj")


        self.df_obv[daily_ret_key] = self.df_obv[self.adj_close_key].pct_change()
        self.df_obv[direction_key] = np.where(self.df_obv[daily_ret_key] >= 0, 1, -1)
        self.df_obv[direction_key][0] = 0
        self.df_obv[volume_adjusted_key] = self.df_obv[self.volume_key] * self.df_obv[direction_key]
        self.df_obv[self.obv_key] = self.df_obv[volume_adjusted_key].cumsum()
        return self.df_obv[self.obv_key]


    # expect Stock, volume, Indicator
    def plot(self, period=100, color="tab:purple"):

        if self.plotter is None:
            print("Please Select the main stock first.")
            raise IOError

        max_value = self.df_obv[self.obv_key].max()
        min_value = self.df_obv[self.obv_key].min()

        if self.plotter.ax_indicators is None or len(self.plotter.ax_indicators) <= 1:
            print("First Indicator OBV")
            self.plotter.ax_indicators[self.obv_key] = self.plotter.ax_indicators[Constants.main_indicator_axis]
        else:
            # instantiate a second axes that shares the same x-axis
            self.plotter.ax_indicators[self.obv_key] = self.plotter.ax_indicators[Constants.main_indicator_axis].twinx()

        self.plotter.ax_indicators[self.obv_key].set_ylim(min_value - 1, max_value + 1)

        self.plotter.ax_indicators[self.obv_key].legend(loc="best")

        self.plotter.main_ax_indicator = self.plotter.ax_indicators[self.obv_key]

        self.plotter.plot_indicator(df=self.df_obv[[self.obv_key]], period=period, color=color)
