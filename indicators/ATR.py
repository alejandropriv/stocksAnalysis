from plotter.Plotter import Plotter
from utilities.Constants import Constants


class ATR:

    ### price is Dataframe
    def __init__(self, high, low, adj_close, n, plotter=None):
        self.n = n
        self.high = high
        self.low = low
        self.adj_close = adj_close

        self.atr_key = None
        self.signal_key = None


        if plotter is None:
            self.plotter = Plotter()
        else:
            self.plotter = plotter

    def calculate(self):
        """function to calculate True Range and Average True Range"""

        df_atr = self.low.iloc[:, [0]].copy()
        ticker = df_atr.columns[0]

        low_key = "{}_{}".format(ticker, "Low")
        high_key = "{}_{}".format(ticker, "High")
        adj_close_key = "{}_{}".format(ticker, "Adj_Close")
        h_l_key = "{}_{}".format(ticker, "H-L")
        h_pc_key = "{}_{}".format(ticker, "H-PC")
        l_pc_key = "{}_{}".format(ticker, "L-PC")
        tr_key = "{}_{}".format(ticker, "TR")
        self.atr_key = "{}_{}".format(ticker, "ATR")

        df_atr.rename(columns={ticker: low_key}, inplace=True)

        df_atr[high_key] = self.high.iloc[:, [0]].copy()
        df_atr[adj_close_key] = self.adj_close.iloc[:, [0]].copy()

        df_atr[h_l_key] = abs(df_atr[high_key] - df_atr[low_key])
        df_atr[h_pc_key] = abs(df_atr[high_key] - df_atr[adj_close_key].shift(1))
        df_atr[l_pc_key] = abs(df_atr[low_key] - df_atr[adj_close_key].shift(1))
        df_atr[tr_key] = df_atr[[h_l_key, h_pc_key, l_pc_key]].max(axis=1, skipna=False)
        df_atr[self.atr_key] = df_atr[tr_key].rolling(self.n).mean()
        # df[atr_key] = df[tr_key].ewm(span=n,adjust=False,min_periods=n).mean()

        df_atr.dropna(inplace=True)

        df_atr2 = df_atr.drop([h_l_key, h_pc_key, l_pc_key], axis=1)
        return df_atr2

    # expect Stock, volume, Indicator
    def plot_atr(self, df, period=100, ticker="", color="tab:green"):

        self.plotter.plot_main(df=df, period=period, ticker=ticker)

        df_atr = df[[self.atr_key]]
        max_value = df_atr[self.atr_key].max()
        min_value = df_atr[self.atr_key].min()


        if self.plotter.ax_indicators is None or len(self.plotter.ax_indicators) <= 1:
            print("First Indicator MACD")
            self.plotter.ax_indicators[self.atr_key] = self.plotter.ax_indicators[Constants.main]
        else:
            # instantiate a second axes that shares the same x-axis
            self.plotter.ax_indicators[self.atr_key] = self.plotter.ax_indicators[Constants.main].twinx()


        self.plotter.ax_indicators[self.atr_key].set_ylim(max_value+1, min_value-1)

        self.plotter.plot_indicator(df=df_atr, period=period, color=color)

        self.plotter.ax_indicators[self.atr_key].legend(loc="upper left")

