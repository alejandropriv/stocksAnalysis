from utilities.Constants import Constants
from indicators.Indicator import Indicator


class MACD(Indicator):

    # price is DataFrame, = adj_close
    def __init__(self, df=None, fast_period=12, slow_period=26, signal_period=9):
        super().__init__()


        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

        # Set dataframe keys
        self.adj_close_key = None
        self.macd_key = None
        self.signal_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataFrame keys
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.macd_key = Constants.get_key(self.ticker, "MACD")
        self.signal_key = Constants.get_key(self.ticker, "Signal")

        self.df = df[[self.adj_close_key]].copy()
        self.df.ticker = df.ticker



    def calculate(self):
        """function to calculate MACD
           typical values a = 12; b =26, c =9"""

        # Set temp dataframe keys
        fast_key = Constants.get_key(self.ticker, "MA_Fast")
        slow_key = Constants.get_key(self.ticker, "MA_Slow")

        self.df[fast_key] = self.df[self.adj_close_key].ewm(span=self.fast_period,
                                                            min_periods=self.fast_period).mean()

        self.df[slow_key] = self.df[self.adj_close_key].ewm(span=self.slow_period,
                                                            min_periods=self.slow_period).mean()

        self.df[self.macd_key] = self.df[fast_key] - self.df[slow_key]

        self.df[self.signal_key] = self.df[self.macd_key].ewm(span=self.signal_period,
                                                              min_periods=self.signal_period).mean()

        self.df.drop(columns=[fast_key, slow_key], inplace=True)

        self.df.dropna(inplace=True)

        return self.df


    def plot(self, plotter=None, period=100, color="tab:green"):

        super().plot(plotter=plotter, period=period, color=color)

        self.plot_indicator(
            plotter=plotter,
            period=period,
            key=self.macd_key,
            color=color,
            legend_position=None
        )

        # TODO: put this inside stock class as a dependency of the indicator
        #plotter.plot_indicator(df=self.df[[self.signal_key]], period=period, color="tab:orange")



