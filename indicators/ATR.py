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

        self.df = df

        if self.df is not None:
            self.set_input_data(self.df)


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
        self.df.ticker = self.ticker


    def calculate(self):
        """function to calculate True Range and Average True Range"""

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

        print("Plotting ATR")
        if plotter is None:
            print("Please Select the main stock first.")
            raise IOError


        max_value = self.df[self.atr_key].max()
        min_value = self.df[self.atr_key].min()


        if plotter.ax_indicators is None or len(plotter.ax_indicators) <= 1:
            print("First Indicator ATR")
            plotter.ax_indicators[self.atr_key] = plotter.ax_indicators[Constants.main_indicator_axis]

        else:
            # instantiate a second axes that shares the same x-axis
            plotter.ax_indicators[self.atr_key] = \
                plotter.ax_indicators[Constants.main_indicator_axis].twinx()



        plotter.ax_indicators[self.atr_key].set_ylim(min_value-1, max_value+1)

        plotter.main_ax_indicator = plotter.ax_indicators[self.atr_key]
        plotter.main_ax_indicator.tick_params(axis='y', labelcolor=color, size=20)


        plotter.plot_indicator(df=self.df[[self.atr_key]], period=period, color=color)

        plotter.main_ax_indicator.legend(loc="upper left")


        return plotter
