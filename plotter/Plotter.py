import matplotlib.pyplot as plt
from utilities.Constants import Constants
import matplotlib.gridspec as gridspec



class Plotter:

    def __init__(self):

        self.fig = None
        self.ax_main = None
        self.ax_indicators = None
        self.main_ax_indicator = None
        self.ticker = None
        self.index = None
        self.i_axes = 0

    def plot_main(self, df, period=100, ticker="", color="black"):

        if ticker is None or ticker is "":
            print("There is no ticker Information, nothing to be plot")
            return

        self.ticker = ticker[0]

        x = df.iloc[:, [0]]
        self.index = x.iloc[-period:, :].index

        if self.fig is None or self.ax_main is None or self.ax_indicators is None:

            adj_close_key = Constants.get_adj_close_key(ticker=self.ticker)

            volume_key = Constants.get_volume_key(ticker=self.ticker)

            time_series_adj_close = df.iloc[-period:, :][adj_close_key]

            time_series_volume = df.iloc[-period:, :][volume_key]

            self.ax_main = dict()
            self.ax_indicators = dict()

            # Plot Line1 (Left Y Axis)
            self.fig, (self.ax_main[Constants.volume], self.ax_indicators[Constants.main_indicator_axis]) = \
                plt.subplots(2,
                             1,
                             figsize=(16, 9),
                             dpi=80,
                             sharex=True,
                             gridspec_kw={'height_ratios': [1, 0]})


            self.set_volume(time_series_volume)

            self.set_stock_price(time_series_adj_close, color)


        else:  # here goes code
            print("Main stock data has already been set.")

    def set_volume(self, time_series_volume):
        self.ax_main[Constants.volume].set_ylim(0, 100000000)
        self.ax_main[Constants.volume].tick_params(axis='y', rotation=0, labelcolor='tab:blue')

        self.ax_main[Constants.volume].spines["top"].set_alpha(0.0)
        self.ax_main[Constants.volume].spines["bottom"].set_alpha(1)
        self.ax_main[Constants.volume].spines["right"].set_alpha(0.0)
        self.ax_main[Constants.volume].spines["left"].set_alpha(1)

        self.ax_main[Constants.volume].bar(self.index, time_series_volume, color='tab:blue', alpha=0.5)
        self.ax_main[Constants.volume].legend()

    def set_stock_price(self, time_series_adj_close, color="black"):

        # Decorations
        # ax1 (left Y axis)
        # instantiate a second axes that shares the same x-axis
        self.ax_main[Constants.adj_close] = self.ax_main[Constants.volume].twinx()

        title = "{}".format(self.ticker)

        self.ax_main[Constants.adj_close].set_title(title, fontsize=22)
        self.ax_main[Constants.adj_close].tick_params(axis='x', rotation=0, labelsize=12, labelleft=True)
        self.ax_main[Constants.adj_close].set_ylabel('Price', color='black', fontsize=20)
        self.ax_main[Constants.adj_close].tick_params(axis='y', rotation=0, labelcolor=color)
        self.ax_main[Constants.adj_close].grid(alpha=.4)

        self.ax_main[Constants.adj_close].spines["top"].set_alpha(0.0)
        self.ax_main[Constants.adj_close].spines["bottom"].set_alpha(1)
        self.ax_main[Constants.adj_close].spines["right"].set_alpha(0.0)
        self.ax_main[Constants.adj_close].spines["left"].set_alpha(1)

        self.ax_main[Constants.adj_close].plot(self.index, time_series_adj_close, color=color)
        self.ax_main[Constants.adj_close].legend()

        #  Set the layout of the indicators plot
        #  Indicator plot layout
        self.ax_indicators[Constants.main_indicator_axis].tick_params(axis='y', labelcolor='tab:green', size=20)
        self.ax_indicators[Constants.main_indicator_axis].grid(alpha=.4)
        self.ax_indicators[Constants.main_indicator_axis].spines["top"].set_alpha(0.0)
        self.ax_indicators[Constants.main_indicator_axis].spines["bottom"].set_alpha(1)
        self.ax_indicators[Constants.main_indicator_axis].spines["right"].set_alpha(0.0)
        self.ax_indicators[Constants.main_indicator_axis].spines["left"].set_alpha(1)



    # this has to be called after calling plot_main
    def plot_indicator(self, df, period=100, color="tab:green"):

        if self.fig is None or\
                self.ax_indicators is None or\
                self.ax_main is None:

            print("Please call first method plot_main")
            return

        print("Plotting MACD")

        indicator_key = df.columns[0]

        max_value = df[indicator_key].max()
        min_value = df[indicator_key].min()

        gs = gridspec.GridSpec(ncols=1, nrows=2, figure=self.fig) #self.fig.add_gridspec(1, 2)


        ax = self.fig.add_subplot(gs[0,1])

        # if self.ax_indicators is None or len(self.ax_indicators) <= 1:
        #
        #     self.ax_indicators[indicator_key] = self.ax_indicators[Constants.main_indicator_axis]
        #
        # else:
        #
        #     # instantiate a second axes that shares the same x-axis
        #     self.ax_indicators[indicator_key] = \
        #         self.ax_indicators[Constants.main_indicator_axis].twinx()

        ax.set_ylim(min_value - 1, max_value + 1)

        ax.tick_params(axis='y', labelcolor=color, size=20)
        # self.plot_indicator(df=self.df_macd[[self.macd_key]], period=period, color=color)
        # self.plot_indicator(df=self.df_macd[[self.signal_key]], period=period, color="tab:orange")


        ax.tick_params(axis='y', labelcolor=color, size=20)
        # title = "{}".format(self.ticker)


        time_series_indicator = df.iloc[-period:, :][indicator_key]

        # Plot Line2 (Right Y Axis)
        self.fig.tight_layout()

        ax.plot(self.index, time_series_indicator, color=color)

        ax.legend(loc="best")
