from utilities.Constants import Constants
import numpy as np
from indicators.ATR import ATR
from indicators.Indicator import Indicator



class ADX(Indicator):

    # price is Dataframe
    def __init__(self, df=None, n=14):

        super().__init__()

        self.n = n

        # Set dataframe keys
        self.low_key = None
        self.high_key = None
        self.adj_close_key = None
        self.adx_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataFrame keys
        self.low_key = Constants.get_low_key(self.ticker)
        self.high_key = Constants.get_high_key(self.ticker)
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.adx_key = Constants.get_key(self.ticker, "ADX")

        self.df = df[[self.low_key]].copy()
        self.df[self.high_key] = df[[self.high_key]]
        self.df[self.adj_close_key] = df[[self.adj_close_key]]
        self.df.ticker = self.ticker


    def calculate(self):
        """"function to calculate ADX"""

        if self.df is None:
            print("DF has not been set, there is no data to calculate the indicator")
            return


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

        atr_ind = ATR(df=self.df, n=14)

        # the period parameter of ATR function does not matter because period does not influence TR calculation
        self.df[tr_key] = atr_ind.calculate()[[tr_key]]

        self.df[dm_plus_key] = \
            np.where(
                (self.df[self.high_key] - self.df[self.high_key].shift(1)) >
                (self.df[self.low_key].shift(1) - self.df[self.low_key]),
                self.df[self.high_key] - self.df[self.high_key].shift(1),
                0)

        self.df[dm_plus_key] = \
            np.where(
                self.df[dm_plus_key] < 0,
                0,
                self.df[dm_plus_key])

        self.df[dm_minus_key] = \
            np.where((self.df[self.low_key].shift(1) - self.df[self.low_key]) >
                     (self.df[self.high_key] - self.df[self.high_key].shift(1)),
                     self.df[self.low_key].shift(1) - self.df[self.low_key],
                     0)

        self.df[dm_minus_key] = np.where(self.df[dm_minus_key] < 0, 0, self.df[dm_minus_key])

        TRn = []
        DMplusN = []
        DMminusN = []
        TR = self.df[tr_key].tolist()
        DMplus = self.df[dm_plus_key].tolist()
        DMminus = self.df[dm_minus_key].tolist()

        for i in range(len(self.df)):
            if i < self.n:
                TRn.append(np.NaN)
                DMplusN.append(np.NaN)
                DMminusN.append(np.NaN)
            elif i == self.n:
                TRn.append(self.df[tr_key].rolling(self.n).sum().tolist()[self.n])
                DMplusN.append(self.df[dm_plus_key].rolling(self.n).sum().tolist()[self.n])
                DMminusN.append(self.df[dm_minus_key].rolling(self.n).sum().tolist()[self.n])
            elif i > self.n:
                TRn.append(TRn[i - 1] - (TRn[i - 1] / 14) + TR[i])
                DMplusN.append(DMplusN[i - 1] - (DMplusN[i - 1] / 14) + DMplus[i])
                DMminusN.append(DMminusN[i - 1] - (DMminusN[i - 1] / 14) + DMminus[i])

        self.df[trn_key] = np.array(TRn)
        self.df[dm_plus_n_key] = np.array(DMplusN)
        self.df[dm_minus_n_key] = np.array(DMminusN)
        self.df[di_plus_n_key] = 100 * (self.df[dm_plus_n_key] / self.df[trn_key])
        self.df[di_minus_n_key] = 100 * (self.df[dm_minus_n_key] / self.df[trn_key])
        self.df[di_diff_key] = abs(self.df[di_plus_n_key] - self.df[di_minus_n_key])
        self.df[di_sum_key] = self.df[di_plus_n_key] + self.df[di_minus_n_key]
        self.df[dx_key] = 100 * (self.df[di_diff_key] / self.df[di_sum_key])
        ADX = []
        DX = self.df[dx_key].tolist()
        for j in range(len(self.df)):
            if j < 2 * self.n - 1:
                ADX.append(np.NaN)
            elif j == 2 * self.n - 1:
                ADX.append(self.df[dx_key][j - self.n + 1:j + 1].mean())
            elif j > 2 * self.n - 1:
                ADX.append(((self.n - 1) * ADX[j - 1] + DX[j]) / self.n)
        self.df[self.adx_key] = np.array(ADX)
        return self.df[self.adx_key]


    # expect Stock, volume, Indicator
    def plot(self, plotter=None, period=100, color="tab:brown"):
        super.
        self.plot_indicator(
            plotter=plotter,
            period=period,
            key=self.adx_key,
            color=color,
            legend_position=None
        )
        #self.plot(plotter=plotter, period=period, key=self.adx_key, color=color)

        print("Plotting ADX")

        max_value = self.df[self.adx_key].max()
        min_value = self.df[self.adx_key].min()

        if plotter.ax_indicators is None or len(plotter.ax_indicators) <= 1:
            print("First Indicator ADX")
            plotter.ax_indicators[self.adx_key] = plotter.ax_indicators[Constants.main_indicator_axis]

        else:
            # instantiate a second axes that shares the same x-axis
            plotter.ax_indicators[self.adx_key] = plotter.ax_indicators[Constants.main_indicator_axis].twinx()

        plotter.ax_indicators[self.adx_key].set_ylim(min_value - 1, max_value + 1)

        plotter.ax_indicators[self.adx_key].legend(loc="best")

        plotter.main_ax_indicator = plotter.ax_indicators[self.adx_key]

        plotter.plot_indicator(df=self.df[[self.adx_key]], period=period, color=color)
