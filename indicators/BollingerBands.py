from plotter.Plotter import Plotter
from utilities.Constants import Constants


class BollingerBands:

    # price is Dataframe
    def __init__(self, adj_close, n=20, plotter=None):
        self.n = n
        self.adj_close = adj_close

        self.bb_up_key = None
        self.bb_down_key = None
        self.bb_width_key = None

        if plotter is None:
            self.plotter = Plotter()
        else:
            self.plotter = plotter


    def calculate(self):
        """function to calculate Bollinger Bands"""

        df_bb = self.adj_close.iloc[:, [0]].copy()

        ticker = df_bb.columns[0]


        adj_close_key = "{}_{}".format(ticker, "Adj_Close")
        ma_key = "{}_{}".format(ticker, "MA")
        self.bb_up_key = "{}_{}".format(ticker, "BB_up")
        self.bb_down_key = "{}_{}".format(ticker, "BB_down")
        self.bb_width_key = "{}_{}".format(ticker, "BB_width")

        df_bb.rename(columns={ticker: adj_close_key}, inplace=True)

        df_bb[ma_key] = df_bb[adj_close_key].rolling(self.n).mean()

        # ddof=0 is required since we want to take the standard deviation of the population and not sample
        df_bb[self.bb_up_key] = df_bb[ma_key] + 2 * df_bb[adj_close_key].rolling(self.n).std(ddof=0)

        # ddof=0 is required since we want to take the standard deviation of the population and not sample
        df_bb[self.bb_down_key] = df_bb[ma_key] - 2 * df_bb[adj_close_key].rolling(self.n).std(
            ddof=0)
        df_bb[self.bb_width_key] = df_bb[self.bb_up_key] - df_bb[self.bb_down_key]
        df_bb.dropna(inplace=True)

        return df_bb


    # expect Stock, volume, Indicator
    def plot_bollinger_bands(self, df, period=100, color="tab:green"):



        x = df.iloc[:, [0]]
        index = x.iloc[-period:, :].index

        # put period for the data also
        df = df.iloc[-period:, :]

        self.plotter.ax_main[Constants.adj_close].plot(index, df[self.bb_down_key], color=color)
        self.plotter.ax_main[Constants.adj_close].plot(index, df[self.bb_up_key], color=color)
