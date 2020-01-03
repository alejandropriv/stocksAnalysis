from utilities.Constants import Constants
import numpy as np


class RSI:

    # price is Dataframe
    def __init__(self, df=None, n=14, plotter=None):

        if df is None:
            print("Error: data not found")
            raise IOError

        self.ticker = df.ticker

        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.rsi_key = Constants.get_key(self.ticker, "RSI")


        self.n = n
        self.adj_close = df[[self.adj_close_key]]

        self.plotter = plotter



    @property
    def calculate(self):
        """"function to calculate RSI"""

        delta_key = Constants.get_key(self.ticker, "delta")
        gain_key = Constants.get_key(self.ticker, "gain")
        loss_key = Constants.get_key(self.ticker, "loss")
        avg_gain_key = Constants.get_key(self.ticker, "avg_gain")
        avg_loss_key = Constants.get_key(self.ticker, "avg_loss")
        rs_key = Constants.get_key(self.ticker, "RS")


        df_rsi = self.adj_close.iloc[:, [0]].copy()
        df_rsi[delta_key] = self.adj_close - self.adj_close.shift(1)
        df_rsi[gain_key] = np.where(df_rsi[delta_key] >= 0, df_rsi[delta_key], 0)
        df_rsi[loss_key] = np.where(df_rsi[delta_key] < 0, abs(df_rsi[delta_key]), 0)
        avg_gain = []
        avg_loss = []
        gain = df_rsi[gain_key].tolist()
        loss = df_rsi[loss_key].tolist()
        for i in range(len(df_rsi)):
            if i < self.n:
                avg_gain.append(np.NaN)
                avg_loss.append(np.NaN)
            elif i == self.n:
                avg_gain.append(df_rsi[gain_key].rolling(self.n).mean().tolist()[self.n])
                avg_loss.append(df_rsi[loss_key].rolling(self.n).mean().tolist()[self.n])
            elif i > self.n:
                avg_gain.append(((self.n - 1) * avg_gain[i - 1] + gain[i]) / self.n)
                avg_loss.append(((self.n - 1) * avg_loss[i - 1] + loss[i]) / self.n)


        df_rsi[avg_gain_key] = np.array(avg_gain)
        df_rsi[avg_loss_key] = np.array(avg_loss)
        df_rsi[rs_key] = df_rsi[avg_gain_key] / df_rsi[avg_loss_key]
        df_rsi[self.rsi_key] = 100 - (100 / (1 + df_rsi[rs_key]))
        return df_rsi[self.rsi_key]


    # expect Stock, volume, Indicator
    def plot(self, df, period=100, color="tab:green"):

        if self.plotter is None:
            print("Please Select the main stock first.")
            raise IOError


        df_rsi = df[[self.rsi_key]]
        max_value = df_rsi[self.rsi_key].max()
        min_value = df_rsi[self.rsi_key].min()


        if self.plotter.ax_indicators is None or len(self.plotter.ax_indicators) <= 1:
            print("First Indicator RSI")
            self.plotter.ax_indicators[self.rsi_key] = self.plotter.ax_indicators[Constants.main_indicator_axis]
        else:
            # instantiate a second axes that shares the same x-axis
            self.plotter.ax_indicators[self.rsi_key] = self.plotter.ax_indicators[Constants.main_indicator_axis].twinx()


        self.plotter.ax_indicators[self.rsi_key].set_ylim(min_value-1, max_value+1)

        self.plotter.ax_indicators[self.rsi_key].legend(loc="best")

        self.plotter.main_ax_indicator = self.plotter.ax_indicators[self.rsi_key]

        self.plotter.plot_indicator(df=df_atr, period=period, color=color)

