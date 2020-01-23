from utilities.Constants import Constants


class MACD:

    # price is Dataframe, = adj_close
    def __init__(self, df=None, fast_period=12, slow_period=26, signal_period=9):
        if df is None:
            print("Error: data not found")
            raise IOError

        self.ticker = df.ticker

        # Set dataframe keys
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)
        self.macd_key = Constants.get_key(self.ticker, "MACD")
        self.signal_key = Constants.get_key(self.ticker, "Signal")

        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

        self.df_macd = df[[self.adj_close_key]].copy()


    def calculate(self):
        """function to calculate MACD
           typical values a = 12; b =26, c =9"""

        # Set temp dataframe keys
        fast_key = Constants.get_key(self.ticker, "MA_Fast")
        slow_key = Constants.get_key(self.ticker, "MA_Slow")

        self.df_macd[fast_key] = self.df_macd[self.adj_close_key].ewm(span=self.fast_period,
                                                                      min_periods=self.fast_period).mean()

        self.df_macd[slow_key] = self.df_macd[self.adj_close_key].ewm(span=self.slow_period,
                                                                      min_periods=self.slow_period).mean()

        self.df_macd[self.macd_key] = self.df_macd[fast_key] - self.df_macd[slow_key]

        self.df_macd[self.signal_key] = self.df_macd[self.macd_key].ewm(span=self.signal_period,
                                                                        min_periods=self.signal_period).mean()

        self.df_macd.drop(columns=[fast_key, slow_key], inplace=True)

        self.df_macd.dropna(inplace=True)

        return self.df_macd

    def plot(self, period=100, plotter=None, color="tab:green"):

        print("Plotting MACD")
        if plotter is None:
            print("Please Select the main stock first.")
            raise IOError


        max_value = self.df_macd[self.macd_key].max()
        min_value = self.df_macd[self.macd_key].min()

        if plotter.ax_indicators is None or len(plotter.ax_indicators) <= 1:

            plotter.ax_indicators[self.macd_key] = plotter.fig.add_subplot(212)
                #plotter.ax_indicators[Constants.main_indicator_axis]

        else:

            # instantiate a second axes that shares the same x-axis
            plotter.ax_indicators[self.macd_key] = \
                plotter.ax_indicators[Constants.main_indicator_axis].twinx()

        plotter.ax_indicators[self.macd_key].set_ylim(min_value - 1, max_value + 1)

        plotter.main_ax_indicator = plotter.ax_indicators[self.macd_key]
        plotter.ax_indicators[self.macd_key].tick_params(axis='y', labelcolor=color, size=20)
        plotter.plot_indicator(df=self.df_macd[[self.macd_key]], period=period, color=color)
        plotter.plot_indicator(df=self.df_macd[[self.signal_key]], period=period, color="tab:orange")

        return plotter
