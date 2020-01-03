from plotter.Plotter import Plotter
from utilities.Constants import Constants


class BollingerBands:

    # price is Dataframe
    def __init__(self, df=None, n=20, plotter=None):

        if df is None:
            print("Error: data not found")
            raise IOError

        self.ticker = df.ticker


        # Set dataframe keys
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.bb_up_key = Constants.get_key(self.ticker, "BB_up")
        self.bb_down_key = Constants.get_key(self.ticker, "BB_down")
        self.bb_width_key = Constants.get_key(self.ticker, "BB_width")

        self.n = n
        self.df_bb = df[[self.adj_close_key]].copy()

        self.ticker = df.ticker


        if plotter is None:
            self.plotter = Plotter()
        else:
            self.plotter = plotter


    def calculate(self):
        """function to calculate Bollinger Bands"""

        # Set temp dataframe keys
        adj_close_key = "{}_{}".format(self.ticker, "Adj_Close")
        ma_key = "{}_{}".format(self.ticker, "MA")


        self.df_bb.rename(columns={self.ticker: adj_close_key}, inplace=True)

        self.df_bb[ma_key] = \
            self.df_bb[adj_close_key].rolling(self.n).mean()

        # ddof=0 is required since we want to take the standard deviation of the population and not sample
        self.df_bb[self.bb_up_key] = \
            self.df_bb[ma_key] + 2 * self.df_bb[adj_close_key].rolling(self.n).std(ddof=0)

        # ddof=0 is required since we want to take the standard deviation of the population and not sample
        self.df_bb[self.bb_down_key] = \
            self.df_bb[ma_key] - 2 * self.df_bb[adj_close_key].rolling(self.n).std(
            ddof=0)
        self.df_bb[self.bb_width_key] = self.df_bb[self.bb_up_key] - self.df_bb[self.bb_down_key]
        self.df_bb.dropna(inplace=True)

        return self.df_bb


    # expect Stock, volume, Indicator
    def plot(self, df, period=100, color="tab:green"):



        x = df.iloc[:, [0]]
        index = x.iloc[-period:, :].index

        # put period for the data also
        df = df.iloc[-period:, :]

        self.plotter.ax_main[Constants.adj_close].plot(index, df[self.bb_down_key], color=color)
        self.plotter.ax_main[Constants.adj_close].plot(index, df[self.bb_up_key], color=color)
