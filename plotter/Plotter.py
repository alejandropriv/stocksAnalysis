import matplotlib.pyplot as plt
from utilities.Constants import Constants


class Plotter:

    def __init__(self):

        self.fig = None
        self.ax_main = None
        self.ax_indicators = None
        self.main_ax_indicator = None
        self.ticker = None



    def plot_main(self, df, period=100, ticker="", color="black"):

        if ticker is None or ticker is "":
            print("There is no ticker Information, nothing to be plot")
            return

        if self.ticker is None or self.ticker is "":
            self.ticker = ticker



        x = df.iloc[:, [0]]
        index = x.iloc[-period:, :].index

        if self.fig is None or self.ax_main is None or self.ax_indicators is None:

            adj_close_key = "{}_{}".format(self.ticker, Constants.adj_close)

            volume_key = "{}_{}".format(self.ticker, Constants.volume)

            time_series_adj_close = df.iloc[-period:, :][adj_close_key]

            time_series_volume = df.iloc[-period:, :][volume_key]

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

            self.set_stock_price(index, time_series_adj_close, color)


        else:  # here goes code for i.e bollinger bands
            print("Main stock data has already been set.")


    def set_indicator_in_main_plot(self, index, time_series, color="green"):
        self.ax_main[Constants.adj_close].plot(index, time_series, color=color)
        self.ax_main[Constants.adj_close].legend()



    def set_volume(self, index, time_series_volume):
        self.ax_main[Constants.volume].set_ylim(0, 100000000)
        self.ax_main[Constants.volume].tick_params(axis='y', rotation=0, labelcolor='tab:blue')

        self.ax_main[Constants.volume].spines["top"].set_alpha(0.0)
        self.ax_main[Constants.volume].spines["bottom"].set_alpha(1)
        self.ax_main[Constants.volume].spines["right"].set_alpha(0.0)
        self.ax_main[Constants.volume].spines["left"].set_alpha(1)

        self.ax_main[Constants.volume].bar(index, time_series_volume, color='tab:blue', alpha=0.5)
        self.ax_main[Constants.volume].legend()


    def set_stock_price(self, index, time_series_adj_close, color="black"):

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

        self.ax_main[Constants.adj_close].plot(index, time_series_adj_close, color=color)
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

        # title = "{}".format(self.ticker)

        indicator_key = df.columns[0]

        x = df.iloc[:, [0]]
        x = x.iloc[-period:, :].index
        time_series_indicator = df.iloc[-period:, :][indicator_key]

        # Plot Line2 (Right Y Axis)
        self.fig.tight_layout()


        self.main_ax_indicator.plot(x, time_series_indicator, color=color)

        self.main_ax_indicator.legend(loc="best")


