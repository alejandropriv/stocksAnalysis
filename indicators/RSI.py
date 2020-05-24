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

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataframe keys
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.rsi_key = Constants.get_key(self.ticker, "OBV")

        self.df = df[[self.adj_close_key]].copy()
        self.df.ticker = df.ticker


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


        self.df[delta_key] = self.df[self.adj_close_key] - self.df[self.adj_close_key].shift(1)
        self.df[gain_key] = np.where(self.df[delta_key] >= 0, self.df[delta_key], 0)
        self.df[loss_key] = np.where(self.df[delta_key] < 0, abs(self.df[delta_key]), 0)
        avg_gain = []
        avg_loss = []
        gain = self.df[gain_key].tolist()
        loss = self.df[loss_key].tolist()
        for i in range(len(self.df)):
            if i < self.n:
                avg_gain.append(np.NaN)
                avg_loss.append(np.NaN)
            elif i == self.n:
                avg_gain.append(self.df[gain_key].rolling(self.n).mean().tolist()[self.n])
                avg_loss.append(self.df[loss_key].rolling(self.n).mean().tolist()[self.n])
            elif i > self.n:
                avg_gain.append(((self.n - 1) * avg_gain[i - 1] + gain[i]) / self.n)
                avg_loss.append(((self.n - 1) * avg_loss[i - 1] + loss[i]) / self.n)


        self.df[avg_gain_key] = np.array(avg_gain)
        self.df[avg_loss_key] = np.array(avg_loss)
        self.df[rs_key] = self.df[avg_gain_key] / self.df[avg_loss_key]
        self.df[self.rsi_key] = 100 - (100 / (1 + self.df[rs_key]))
        return self.df[self.rsi_key]


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

