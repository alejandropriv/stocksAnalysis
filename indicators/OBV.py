from utilities.Constants import Constants
import numpy as np
from indicators.ATR import ATR


class ADX:

    # price is Dataframe
    def __init__(self, df=None, n=14, plotter=None):

        if df is None:
            print("Error: data not found")
            raise IOError

        self.ticker = df.ticker

        # Set dataframe keys
        self.low_key = Constants.get_low_key(df.ticker)
        self.high_key = Constants.get_high_key(df.ticker)
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.adx_key = Constants.get_key(self.ticker, "ADX")

        self.n = n
        self.df_adx = df[[self.low_key]].copy()
        self.df_adx[self.high_key] = df[[self.high_key]]
        self.df_adx[self.adj_close_key] = df[[self.adj_close_key]]
        self.df_adx.ticker = df.ticker

        self.plotter = plotter

    def calculate(self):
        """"function to calculate ADX"""

        tr_key = Constants.get_key(self.ticker, "TR")
        trn_key = Constants.get_key(self.ticker, "TRn")

        dm_plus_key = Constants.get_key(self.ticker, "DMplus")
        dm_plus_n_key = Constants.get_key(self.ticker, "DMplusN")

        dm_minus_key = Constants.get_key(self.ticker, "DMminus")
        dm_minus_n_key = Constants.get_key(self.ticker, "DMminusN")
        di_plus_n_key = Constants.get_key(self.ticker, "DIplusN")
        di_minus_n_key = Constants.get_key(self.ticker, "DIminusN")
        di_diff_key = Constants.get_key(self.ticker, "DIdiff")
        di_sum_key = Constants.get_key(self.ticker, "DIsum")
        dx_key = Constants.get_key(self.ticker, "DX")

        atr_ind = ATR(df=self.df_adx, n=14)

        # the period parameter of ATR function does not matter because period does not influence TR calculation
        self.df_adx[tr_key] = atr_ind.calculate()[[tr_key]]

        self.df_adx[dm_plus_key] = \
            np.where(
                (self.df_adx[self.high_key] - self.df_adx[self.high_key].shift(1)) >
                (self.df_adx[self.low_key].shift(1) - self.df_adx[self.low_key]),
                self.df_adx[self.high_key] - self.df_adx[self.high_key].shift(1),
                0)

        self.df_adx[dm_plus_key] = \
            np.where(
                self.df_adx[dm_plus_key] < 0,
                0,
                self.df_adx[dm_plus_key])

        self.df_adx[dm_minus_key] = \
            np.where((self.df_adx[self.low_key].shift(1) - self.df_adx[self.low_key]) >
                     (self.df_adx[self.high_key] - self.df_adx[self.high_key].shift(1)),
                     self.df_adx[self.low_key].shift(1) - self.df_adx[self.low_key],
                     0)

        self.df_adx[dm_minus_key] = np.where(self.df_adx[dm_minus_key] < 0, 0, self.df_adx[dm_minus_key])

        TRn = []
        DMplusN = []
        DMminusN = []
        TR = self.df_adx[tr_key].tolist()
        DMplus = self.df_adx[dm_plus_key].tolist()
        DMminus = self.df_adx[dm_minus_key].tolist()

        for i in range(len(self.df_adx)):
            if i < self.n:
                TRn.append(np.NaN)
                DMplusN.append(np.NaN)
                DMminusN.append(np.NaN)
            elif i == self.n:
                TRn.append(self.df_adx[tr_key].rolling(self.n).sum().tolist()[self.n])
                DMplusN.append(self.df_adx[dm_plus_key].rolling(self.n).sum().tolist()[self.n])
                DMminusN.append(self.df_adx[dm_minus_key].rolling(self.n).sum().tolist()[self.n])
            elif i > self.n:
                TRn.append(TRn[i - 1] - (TRn[i - 1] / 14) + TR[i])
                DMplusN.append(DMplusN[i - 1] - (DMplusN[i - 1] / 14) + DMplus[i])
                DMminusN.append(DMminusN[i - 1] - (DMminusN[i - 1] / 14) + DMminus[i])

        self.df_adx[trn_key] = np.array(TRn)
        self.df_adx[dm_plus_n_key] = np.array(DMplusN)
        self.df_adx[dm_minus_n_key] = np.array(DMminusN)
        self.df_adx[di_plus_n_key] = 100 * (self.df_adx[dm_plus_n_key] / self.df_adx[trn_key])
        self.df_adx[di_minus_n_key] = 100 * (self.df_adx[dm_minus_n_key] / self.df_adx[trn_key])
        self.df_adx[di_diff_key] = abs(self.df_adx[di_plus_n_key] - self.df_adx[di_minus_n_key])
        self.df_adx[di_sum_key] = self.df_adx[di_plus_n_key] + self.df_adx[di_minus_n_key]
        self.df_adx[dx_key] = 100 * (self.df_adx[di_diff_key] / self.df_adx[di_sum_key])
        ADX = []
        DX = self.df_adx[dx_key].tolist()
        for j in range(len(self.df_adx)):
            if j < 2 * self.n - 1:
                ADX.append(np.NaN)
            elif j == 2 * self.n - 1:
                ADX.append(self.df_adx[dx_key][j - self.n + 1:j + 1].mean())
            elif j > 2 * self.n - 1:
                ADX.append(((self.n - 1) * ADX[j - 1] + DX[j]) / self.n)
        self.df_adx[self.adx_key] = np.array(ADX)
        return self.df_adx[self.adx_key]

    # expect Stock, volume, Indicator
    def plot(self, period=100, color="tab:green"):

        if self.plotter is None:
            print("Please Select the main stock first.")
            raise IOError

        max_value = self.df_adx[self.adx_key].max()
        min_value = self.df_adx[self.adx_key].min()

        if self.plotter.ax_indicators is None or len(self.plotter.ax_indicators) <= 1:
            print("First Indicator RSI")
            self.plotter.ax_indicators[self.adx_key] = self.plotter.ax_indicators[Constants.main_indicator_axis]
        else:
            # instantiate a second axes that shares the same x-axis
            self.plotter.ax_indicators[self.adx_key] = self.plotter.ax_indicators[Constants.main_indicator_axis].twinx()

        self.plotter.ax_indicators[self.adx_key].set_ylim(min_value - 1, max_value + 1)

        self.plotter.ax_indicators[self.adx_key].legend(loc="best")

        self.plotter.main_ax_indicator = self.plotter.ax_indicators[self.adx_key]

        self.plotter.plot_indicator(df=self.df_adx[[self.adx_key]], period=period, color=color)
