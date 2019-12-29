from utilities.Constants import Constants


class MACD:

    # price is Dataframe, = adj_close
    def __init__(self, price, fast_period=12, slow_period=26, signal_period=9, plotter=None):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

        self.price = price

        self.macd_key = None
        self.signal_key = None

        self.plotter = plotter


    def calculate(self):
        """function to calculate MACD
           typical values a = 12; b =26, c =9"""

        df_macd = self.price.iloc[:, [0]].copy()
        price_key = df_macd.ticker

        fast_key = "{}_{}".format(price_key, "MA_Fast")
        slow_key = "{}_{}".format(price_key, "MA_Slow")
        self.macd_key = "{}_{}".format(price_key, "MACD")
        self.signal_key = "{}_{}".format(price_key, "Signal")

        df_macd[fast_key] = df_macd[price_key].ewm(span=self.fast_period,
                                                   min_periods=self.fast_period).mean()

        df_macd[slow_key] = df_macd[price_key].ewm(span=self.slow_period,
                                                   min_periods=self.slow_period).mean()

        df_macd[self.macd_key] = df_macd[fast_key] - df_macd[slow_key]

        df_macd[self.signal_key] = df_macd[self.macd_key].ewm(span=self.signal_period,
                                                              min_periods=self.signal_period).mean()

        df_macd.drop(columns=[fast_key, slow_key], inplace=True)

        df_macd.dropna(inplace=True)  # TODO: check if no extra data is lost in each iteration

        return df_macd

    def plot_macd(self, df, period=100, color="tab:green"):

        if self.plotter is None:
            print("Please Select the main stock first.")
            return


        df_macd = df[[self.macd_key]]
        df_macd_signal = df[[self.signal_key]]
        max_value = df_macd[self.macd_key].max()
        min_value = df_macd[self.macd_key].min()


        if self.plotter.ax_indicators is None or len(self.plotter.ax_indicators) <= 1:
            print("First Indicator MACD")
            self.plotter.ax_indicators[self.macd_key] = self.plotter.ax_indicators[Constants.main]

        else:
            # instantiate a second axes that shares the same x-axis
            self.plotter.ax_indicators[self.macd_key] = self.plotter.ax_indicators[Constants.main].twinx()


        self.plotter.ax_indicators[self.macd_key].set_ylim(min_value-1, max_value+1)

        self.plotter.main_ax_indicator = self.plotter.ax_indicators[self.macd_key]
        self.plotter.plot_indicator(df=df_macd, period=period, color=color)
        self.plotter.plot_indicator(df=df_macd_signal, period=period, color="tab:orange")

