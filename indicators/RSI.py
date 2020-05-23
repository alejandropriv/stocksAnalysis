from utilities.Constants import Constants
import numpy as np
from indicators.Indicator import Indicator


class RSI(Indicator):

    # price is Dataframe
    def __init__(self, df=None, n=14):
        super().__init__()

        self.n = n

        # Set dataframe keys
        self.adj_close_key = None
        self.rsi_key = None

        self.df = df

        if self.df is not None:
            df.set_input_data(self.df)



    def calculate(self):

        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.rsi_key = Constants.get_key(self.ticker, "RSI")

        """"function to calculate RSI"""

        delta_key = Constants.get_key(self.ticker, "delta")
        gain_key = Constants.get_key(self.ticker, "gain")
        loss_key = Constants.get_key(self.ticker, "loss")
        avg_gain_key = Constants.get_key(self.ticker, "avg_gain")
        avg_loss_key = Constants.get_key(self.ticker, "avg_loss")
        rs_key = Constants.get_key(self.ticker, "RS")


        self.df_rsi[delta_key] = self.df_rsi[self.adj_close_key] - self.df_rsi[self.adj_close_key].shift(1)
        self.df_rsi[gain_key] = np.where(self.df_rsi[delta_key] >= 0, self.df_rsi[delta_key], 0)
        self.df_rsi[loss_key] = np.where(self.df_rsi[delta_key] < 0, abs(self.df_rsi[delta_key]), 0)
        avg_gain = []
        avg_loss = []
        gain = self.df_rsi[gain_key].tolist()
        loss = self.df_rsi[loss_key].tolist()
        for i in range(len(self.df_rsi)):
            if i < self.n:
                avg_gain.append(np.NaN)
                avg_loss.append(np.NaN)
            elif i == self.n:
                avg_gain.append(self.df_rsi[gain_key].rolling(self.n).mean().tolist()[self.n])
                avg_loss.append(self.df_rsi[loss_key].rolling(self.n).mean().tolist()[self.n])
            elif i > self.n:
                avg_gain.append(((self.n - 1) * avg_gain[i - 1] + gain[i]) / self.n)
                avg_loss.append(((self.n - 1) * avg_loss[i - 1] + loss[i]) / self.n)


        self.df_rsi[avg_gain_key] = np.array(avg_gain)
        self.df_rsi[avg_loss_key] = np.array(avg_loss)
        self.df_rsi[rs_key] = self.df_rsi[avg_gain_key] / self.df_rsi[avg_loss_key]
        self.df_rsi[self.rsi_key] = 100 - (100 / (1 + self.df_rsi[rs_key]))
        return self.df_rsi[self.rsi_key]


    # expect Stock, volume, Indicator
    def plot(self, period=100, color="tab:green"):

        if self.plotter is None:
            print("Please Select the main stock first.")
            raise IOError


        max_value = self.df_rsi[self.rsi_key].max()
        min_value = self.df_rsi[self.rsi_key].min()


        if self.plotter.ax_indicators is None or len(self.plotter.ax_indicators) <= 1:
            print("First Indicator RSI")
            self.plotter.ax_indicators[self.rsi_key] = self.plotter.ax_indicators[Constants.main_indicator_axis]
        else:
            # instantiate a second axes that shares the same x-axis
            self.plotter.ax_indicators[self.rsi_key] = self.plotter.ax_indicators[Constants.main_indicator_axis].twinx()


        self.plotter.ax_indicators[self.rsi_key].set_ylim(min_value-1, max_value+1)

        self.plotter.ax_indicators[self.rsi_key].legend(loc="best")

        self.plotter.main_ax_indicator = self.plotter.ax_indicators[self.rsi_key]
        self.plotter.ax_indicators[self.rsi_key].tick_params(axis='y', labelcolor=color, size=20)


        self.plotter.plot_indicator(df=self.df_rsi[[self.rsi_key]], period=period, color=color)

