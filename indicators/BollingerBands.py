from plotter.Plotter import Plotter
from utilities.Constants import Constants
from indicators.Indicator import Indicator



class BollingerBands(Indicator):

    # price is Dataframe
    def __init__(self, df=None, n=20):
        super().__init__()

        self.n = n

        if df is None:
            print("Error: data not found")
            raise IOError

        self.ticker = df.ticker


        # Set dataframe keys
        self.adj_close_key = None
        self.bb_up_key = None
        self.bb_down_key = None
        self.bb_width_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataframe keys
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.bb_up_key = Constants.get_key(self.ticker, "BB_up")
        self.bb_down_key = Constants.get_key(self.ticker, "BB_down")
        self.bb_width_key = Constants.get_key(self.ticker, "BB_width")

        self.df = df[[self.adj_close_key]].copy()

        self.df.ticker = df.ticker




    def calculate(self):
        """function to calculate Bollinger Bands"""

        # Set temp dataframe keys
        ma_key = Constants.get_key(self.ticker, "MA")


        self.df.rename(columns={self.ticker: self.adj_close_key}, inplace=True)

        self.df[ma_key] = \
            self.df[self.adj_close_key].rolling(self.n).mean()

        # ddof=0 is required since we want to take the standard deviation of the population and not sample
        self.df[self.bb_up_key] = \
            self.df[ma_key] + 2 * self.df[self.adj_close_key].rolling(self.n).std(ddof=0)

        # ddof=0 is required since we want to take the standard deviation of the population and not sample
        self.df[self.bb_down_key] = \
            self.df[ma_key] - 2 * self.df[self.adj_close_key].rolling(self.n).std(
            ddof=0)
        self.df[self.bb_width_key] = self.df[self.bb_up_key] - self.df[self.bb_down_key]
        self.df.dropna(inplace=True)

        return self.df


    # expect Stock, volume, Indicator
    def plot(self,  plotter=None, period=100, color="tab:green"):
        super().plot(plotter=plotter, period=period, color=color)

        x = self.df.iloc[:, [0]]
        index = x.iloc[-period:, :].index

        # put period for the data also
        df = self.df.iloc[-period:, :]

        plotter.ax_main[Constants.adj_close].plot(index, df[self.bb_down_key], color=color)
        plotter.ax_main[Constants.adj_close].plot(index, df[self.bb_up_key], color=color)
