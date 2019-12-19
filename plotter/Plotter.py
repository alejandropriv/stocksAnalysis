import matplotlib.pyplot as plt
from utilities.Constants import Constants


class Plotter:

    def __init__(self):

        self.fig = None
        self.ax_main = None
        self.ax_indicators = None
        self.ticker = None

    def set_existing_plot(self, ticker, fig, ax_main, ax_indicators):
        self.fig = fig
        self.ax_main = ax_main
        self.ax_indicators = ax_indicators
        self.ticker = ticker

    def plot_main(self, df, period=100, ticker=""):

        if ticker is None or ticker is "":
            print("There is no ticker Information, nothing to be plot")
            return

        if self.ticker is None or self.ticker is "":
            self.ticker = ticker

        adj_close_key = "{}_{}".format(self.ticker, Constants.adj_close)

        volume_key = "{}_{}".format(self.ticker, Constants.volume)

        time_series_adj_close = df.iloc[-period:, :][adj_close_key]

        time_series_volume = df.iloc[-period:, :][volume_key]



        if self.fig is None or self.ax_main is None or self.ax_indicators is None:
            x = df.iloc[:, [0]]
            index = x.iloc[-period:, :].index

            self.ax_main = dict()
            self.ax_indicators = dict()

            # Plot Line1 (Left Y Axis)
            self.fig, (self.ax_main[Constants.volume], self.ax_indicators[Constants.main]) = plt.subplots(2,
                                                                               1,
                                                                               figsize=(16, 9),
                                                                               dpi=80,
                                                                               sharex=True,
                                                                               gridspec_kw={'height_ratios': [2, 1]})

            self.set_volume(index, time_series_volume)

            self.set_stock_price(index, time_series_adj_close)


        else:  # here goes code for bollinger bands i.e
            pass

    def set_volume(self, index, time_series_volume):
        self.ax_main[Constants.volume].set_ylim(0, 100000000)
        self.ax_main[Constants.volume].tick_params(axis='y', rotation=0, labelcolor='tab:blue')

        self.ax_main[Constants.volume].spines["top"].set_alpha(0.0)
        self.ax_main[Constants.volume].spines["bottom"].set_alpha(1)
        self.ax_main[Constants.volume].spines["right"].set_alpha(0.0)
        self.ax_main[Constants.volume].spines["left"].set_alpha(1)

        self.ax_main[Constants.volume].bar(index, time_series_volume, color='tab:blue', alpha=0.5)
        self.ax_main[Constants.volume].legend()


    def set_stock_price(self, index, time_series_adj_close):

        # Decorations
        # ax1 (left Y axis)
        # instantiate a second axes that shares the same x-axis
        self.ax_main[Constants.adj_close] = self.ax_main[Constants.volume].twinx()

        title = "{}".format(self.ticker)

        self.ax_main[Constants.adj_close].set_title(title, fontsize=22)
        self.ax_main[Constants.adj_close].tick_params(axis='x', rotation=0, labelsize=12, labelleft=True)
        self.ax_main[Constants.adj_close].set_ylabel('Price', color='black', fontsize=20)
        self.ax_main[Constants.adj_close].tick_params(axis='y', rotation=0, labelcolor='black')
        self.ax_main[Constants.adj_close].grid(alpha=.4)

        self.ax_main[Constants.adj_close].spines["top"].set_alpha(0.0)
        self.ax_main[Constants.adj_close].spines["bottom"].set_alpha(1)
        self.ax_main[Constants.adj_close].spines["right"].set_alpha(0.0)
        self.ax_main[Constants.adj_close].spines["left"].set_alpha(1)

        self.ax_main[Constants.adj_close].plot(index, time_series_adj_close, color='black')
        self.ax_main[Constants.adj_close].legend()

        #  Set the layout of the indicators plot
        #  Indicator plot layout
        self.ax_indicators[Constants.main].tick_params(axis='y', labelcolor='tab:green', size=20)
        self.ax_indicators[Constants.main].grid(alpha=.4)
        self.ax_indicators[Constants.main].spines["top"].set_alpha(0.0)
        self.ax_indicators[Constants.main].spines["bottom"].set_alpha(1)
        self.ax_indicators[Constants.main].spines["right"].set_alpha(0.0)
        self.ax_indicators[Constants.main].spines["left"].set_alpha(1)


    # this has to be called after calling plot_main
    def plot_indicator(self, df, period=100, color="tab:green"):


        if self.fig is None or self.ax_indicators is None:
            print("Please call first method plot_main")
            return

        title = "{}".format(self.ticker)

        indicator_key = df.columns[0]

        x = df.iloc[:, [0]]
        x = x.iloc[-period:, :].index
        time_series_indicator = df.iloc[-period:, :][indicator_key]



        # Plot Line2 (Right Y Axis)
        self.fig.tight_layout()

        self.ax_indicators[indicator_key].plot(x, time_series_indicator, color=color)




    #
    # @staticmethod
    # def plot_bollinger_bands(df, period=100,  title=""):  # TODO: this is not correct
    #
    #     title = "{} {}".format(title, "MACD")
    #
    #     x = df.loc[:, ["FB"]]
    #     x = x.iloc[-period:, :].index
    #     y1 = df.iloc[-period:, 1]
    #     y2 = df.iloc[-period:, 4]
    #
    #     # Plot Line1 (Left Y Axis)
    #     fig, ax1 = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
    #     ax1.plot(x, y1, color='tab:red')
    #
    #     # Plot Line2 (Right Y Axis)
    #     ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    #     ax2.plot(x, y2, color='tab:blue')
    #
    #     # Decorations
    #     # ax1 (left Y axis)
    #     ax1.set_xlabel('Date', fontsize=20)
    #     ax1.tick_params(axis='x', rotation=0, labelsize=12)
    #     ax1.set_ylabel('Stock', color='tab:red', fontsize=20)
    #     ax1.tick_params(axis='y', rotation=0, labelcolor='tab:red')
    #     ax1.grid(alpha=.4)
    #
    #     # ax2 (right Y axis)
    #     ax2.set_ylabel("MACD", color='tab:blue', fontsize=20)
    #     ax2.tick_params(axis='y', labelcolor='tab:blue')
    #     # ax2.set_xticks(np.arange(0, len(x), 60))
    #     # ax2.set_xticklabels(x[::60], rotation=90, fontdict={'fontsize': 10})
    #     ax2.set_title("MACDAX2", fontsize=22)
    #     fig.tight_layout()
    #     plt.show()
