from utilities.Constants import Constants


class ATR:

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
        self.atr_key = Constants.get_key(self.ticker, "ATR")


        self.n = n
        self.df_atr = df[[self.low_key]].copy()
        self.df_atr[self.high_key] = df[[self.high_key]]
        self.df_atr[self.adj_close_key] = df[[self.adj_close_key]]

        self.plotter = plotter

    def calculate(self):
        """function to calculate True Range and Average True Range"""

        # Set temp dataframe keys
        h_l_key = Constants.get_key(self.ticker, "H-L")
        h_pc_key = Constants.get_key(self.ticker, "H-PC")
        l_pc_key = Constants.get_key(self.ticker, "L-PC")
        tr_key = Constants.get_key(self.ticker, "TR")

        self.df_atr[h_l_key] = abs(self.df_atr[self.high_key] - self.df_atr[self.low_key])
        self.df_atr[h_pc_key] = abs(self.df_atr[self.high_key] - self.df_atr[self.adj_close_key].shift(1))
        self.df_atr[l_pc_key] = abs(self.df_atr[self.low_key] - self.df_atr[self.adj_close_key].shift(1))
        self.df_atr[tr_key] = self.df_atr[[h_l_key, h_pc_key, l_pc_key]].max(axis=1, skipna=False)
        self.df_atr[self.atr_key] = self.df_atr[tr_key].rolling(self.n).mean()
        # df[atr_key] = df[tr_key].ewm(span=n,adjust=False,min_periods=n).mean()

        self.df_atr.dropna(inplace=True)

        df_atr2 = self.df_atr.drop([h_l_key, h_pc_key, l_pc_key], axis=1)
        return df_atr2

    # expect Stock, volume, Indicator
    def plot(self, period=100, color="tab:green"):

        if self.plotter is None:
            print("Please Select the main stock first.")
            raise IOError


        max_value = self.df_atr[self.atr_key].max()
        min_value = self.df_atr[self.atr_key].min()


        if self.plotter.ax_indicators is None or len(self.plotter.ax_indicators) <= 1:
            print("First Indicator ATR")
            self.plotter.ax_indicators[self.atr_key] = self.plotter.ax_indicators[Constants.main_indicator_axis]

        else:
            # instantiate a second axes that shares the same x-axis
            self.plotter.ax_indicators[self.atr_key] = \
                self.plotter.ax_indicators[Constants.main_indicator_axis].twinx()


        self.plotter.ax_indicators[self.atr_key].set_ylim(min_value-1, max_value+1)

        self.plotter.ax_indicators[self.atr_key].legend(loc="best")

        self.plotter.main_ax_indicator = self.plotter.ax_indicators[self.atr_key]
        self.plotter.ax_indicators[self.atr_key].tick_params(axis='y', labelcolor=color, size=20)


        self.plotter.plot_indicator(df=self.df_atr[[self.atr_key]], period=period, color=color)

