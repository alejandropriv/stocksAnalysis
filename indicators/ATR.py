from utilities.Constants import Constants
from indicators.Indicator import Indicator


class ATR(Indicator):

    # price is Dataframe
    def __init__(self, df=None, n=14):
        super().__init__()

        self.n = n

        # Set dataframe keys
        self.low_key = None
        self.high_key = None
        self.adj_close_key = None
        self.atr_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataframe keys
        self.low_key = Constants.get_low_key(df.ticker)
        self.high_key = Constants.get_high_key(df.ticker)
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.atr_key = Constants.get_key(self.ticker, "ATR")

        self.df = df[[self.low_key]].copy()
        self.df[self.high_key] = df[[self.high_key]]
        self.df[self.adj_close_key] = df[[self.adj_close_key]]
        self.df.ticker = df.ticker


    def calculate(self):
        """function to calculate True Range and Average True Range"""

        if self.df is None:
            print("DF has not been set, there is no data to calculate the indicator")
            return

        # Set temp dataframe keys
        h_l_key = Constants.get_key(self.ticker, "H-L")
        h_pc_key = Constants.get_key(self.ticker, "H-PC")
        l_pc_key = Constants.get_key(self.ticker, "L-PC")
        tr_key = Constants.get_key(self.ticker, "TR")

        self.df[h_l_key] = abs(self.df[self.high_key] - self.df[self.low_key])
        self.df[h_pc_key] = abs(self.df[self.high_key] - self.df[self.adj_close_key].shift(1))
        self.df[l_pc_key] = abs(self.df[self.low_key] - self.df[self.adj_close_key].shift(1))
        self.df[tr_key] = self.df[[h_l_key, h_pc_key, l_pc_key]].max(axis=1, skipna=False)
        self.df[self.atr_key] = self.df[tr_key].rolling(self.n).mean()
        # df[atr_key] = df[tr_key].ewm(span=n,adjust=False,min_periods=n).mean()

        #self.df.dropna(inplace=True, axis=0)

        self.df.drop([h_l_key, h_pc_key, l_pc_key], axis=1, inplace=True)
        return self.df

    # expect Stock, volume, Indicator
    def plot(self, plotter=None, period=100, color="tab:red"):

        super().plot(plotter=plotter, period=period, color=color)

        self.plot_indicator(
            plotter=plotter,
            period=period,
            key=self.atr_key,
            color=color,
            legend_position=None
        )
