from utilities.Constants import Constants
import numpy as np

from indicators.Indicator import Indicator



class OBV(Indicator):
    #TODO verify the correct data is present
    # df requires:  price adjusted close
    #               volume
    def __init__(self, df=None, n=14):
        super().__init__()

        self.n = n

        # Set dataframe keys
        self.adj_close_key = None
        self.volume_key = None
        self.obv_key = None

        self.df = df

        if self.df is not None:
            df.set_input_data(self.df)



    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataframe keys
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.volume_key = Constants.get_volume_key(self.ticker)
        self.obv_key = Constants.get_key(self.ticker, "OBV")

        self.df = df[[self.adj_close_key]].copy()
        self.df[self.volume_key] = df[[self.volume_key]]
        self.df.ticker = df.ticker

        self.df.ticker = self.ticker



    def calculate(self):
        """function to calculate On Balance Volume"""

        daily_ret_key = Constants.get_key(self.ticker, "daily_ret")
        direction_key = Constants.get_key(self.ticker, "direction")
        volume_adjusted_key = Constants.get_key(self.ticker, "vol_adj")


        self.df[daily_ret_key] = self.df[self.adj_close_key].pct_change()
        self.df[direction_key] = np.where(self.df[daily_ret_key] >= 0, 1, -1)
        #self.df.loc[0, direction_key] = 0
        self.df[direction_key][0] = 0 #TODO check this for copy vs
        self.df[volume_adjusted_key] = self.df[self.volume_key] * self.df[direction_key]
        self.df[self.obv_key] = self.df[volume_adjusted_key].cumsum()
        return self.df[self.obv_key]


    # expect Stock, volume, Indicator
    def plot(self, plotter=None, period=100, color="tab:green"):

        super().plot(plotter=plotter, period=period, color=color)

        print("Plotting OBV")

        max_value = self.df[self.obv_key].max()
        min_value = self.df[self.obv_key].min()

        if plotter.ax_indicators is None or len(plotter.ax_indicators) <= 1:
            print("First Indicator OBV")
            plotter.ax_indicators[self.obv_key] = plotter.ax_indicators[Constants.main_indicator_axis]
        else:
            # instantiate a second axes that shares the same x-axis
            plotter.ax_indicators[self.obv_key] = plotter.ax_indicators[Constants.main_indicator_axis].twinx()

        plotter.ax_indicators[self.obv_key].set_ylim(min_value - 1, max_value + 1)

        plotter.ax_indicators[self.obv_key].legend(loc="best")

        plotter.main_ax_indicator = plotter.ax_indicators[self.obv_key]

        plotter.plot_indicator(df=self.df[[self.obv_key]], period=period, color=color)
