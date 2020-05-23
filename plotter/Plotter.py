import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from utilities.Constants import Constants


class Plotter:




    def get_legend_position(self):
        legend = ["upper right", "upper left", "lower left",
                  "lower right", "right", "center left",
                  "center right", "lower center", "upper center", "center"]

        legend_name = legend[self.legend_id % 10]
        self.legend_id += 1
        return legend_name


    def __init__(self):

        self.fig = None
        self.ax_main = None
        self.ax_indicators = None
        self.main_ax_indicator = None
        self.ticker = None
        self.index = None
        self.legend_id = 0

        register_matplotlib_converters()



    def plot_main(self, df, period=100, color="black"):

        if df.ticker is None or df.ticker is "":
            print("There is no ticker Information, nothing to be plot")
            return

        self.ticker = df.ticker

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
            self.fig, (self.ax_main[Constants.volume], self.ax_indicators[Constants.main_indicator_axis]) = plt.subplots(2,
                                                                                                                         1,
                                                                                                                         figsize=(16, 9),
                                                                                                                         dpi=80,
                                                                                                                         sharex=True,
                                                                                                                         gridspec_kw={'height_ratios': [2, 1]})

            self.set_volume(time_series_volume)

            self.set_stock_price(time_series_adj_close, color)


        else:  # here goes code for i.e bollinger bands
            print("Main stock data has already been set.")



    def set_volume(self, time_series_volume):
        self.ax_main[Constants.volume].set_ylim(0, 100000000)
        self.ax_main[Constants.volume].tick_params(axis='y', rotation=0, labelcolor='tab:blue')

        self.ax_main[Constants.volume].spines["top"].set_alpha(0.0)
        self.ax_main[Constants.volume].spines["bottom"].set_alpha(1)
        self.ax_main[Constants.volume].spines["right"].set_alpha(0.0)
        self.ax_main[Constants.volume].spines["left"].set_alpha(1)

        self.ax_main[Constants.volume].bar(self.index, time_series_volume, color='tab:blue', alpha=0.5, label='Volume')
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


        if self.fig is None or self.ax_indicators is None:
            print("Please call first method plot_main")
            return

        indicator_key = df.columns[0]

        time_series_indicator = df.iloc[-period:, :][indicator_key]

        # Plot Line2 (Right Y Axis)
        self.fig.tight_layout()

        self.main_ax_indicator.plot(self.index, time_series_indicator, color=color)

