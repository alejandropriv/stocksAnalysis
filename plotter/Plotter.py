import matplotlib.pyplot as plt


class Plotter:

    def __init__(self):
        self.fig = None
        self.ax_vol = None
        self.ax_indicator = None
        self.ax_pri = None
        self.ticker = None

    def set_existing_plot(self, ticker, fig, ax_vol, ax_indicator, ax_pri):
        self.fig = fig
        self.ax_vol = ax_vol
        self.ax_indicator = ax_indicator
        self.ax_pri = ax_pri
        self.ticker = ticker

    def plot_main(self, df, period=100, ticker=""):

        if self.ticker is None or self.ticker is "":
            self.ticker = ticker

        title = "{}".format(self.ticker)

        adj_close_key = "{}_{}".format(self.ticker, "Adj_Close")

        volume_key = "{}_{}".format(self.ticker, "Volume")

        time_series_price = df.iloc[-period:, :][adj_close_key]

        time_series_volume = df.iloc[-period:, :][volume_key]

        if self.fig is None or self.ax_vol is None or self.ax_indicator is None:
            x = df.iloc[:, [0]]
            x = x.iloc[-period:, :].index

            # Plot Line1 (Left Y Axis)
            self.fig, (self.ax_vol, self.ax_indicator) = plt.subplots(2,
                                                                      1,
                                                                      figsize=(16, 9),
                                                                      dpi=80,
                                                                      sharex=True,
                                                                      gridspec_kw={'height_ratios': [3, 1]})


            self.ax_vol.set_ylim(0, 100000000)
            self.ax_vol.tick_params(axis='y', rotation=0, labelcolor='tab:blue')

            self.ax_vol.spines["top"].set_alpha(0.0)
            self.ax_vol.spines["bottom"].set_alpha(1)
            self.ax_vol.spines["right"].set_alpha(0.0)
            self.ax_vol.spines["left"].set_alpha(1)

            self.ax_vol.bar(x, time_series_volume, color='tab:blue', alpha=0.5)


            # Decorations
            # ax1 (left Y axis)

            self.ax_pri = self.ax_vol.twinx()  # instantiate a second axes that shares the same x-axis

            self.ax_pri.set_title(title, fontsize=22)
            self.ax_pri.tick_params(axis='x', rotation=0, labelsize=12, labelleft=True)
            self.ax_pri.set_ylabel('Price', color='black', fontsize=20)
            self.ax_pri.tick_params(axis='y', rotation=0, labelcolor='black')
            self.ax_pri.grid(alpha=.4)

            self.ax_pri.spines["top"].set_alpha(0.0)
            self.ax_pri.spines["bottom"].set_alpha(1)
            self.ax_pri.spines["right"].set_alpha(0.0)
            self.ax_pri.spines["left"].set_alpha(1)

            self.ax_pri = self.ax_vol.twinx()  # instantiate a second axes that shares the same x-axis
            self.ax_pri.plot(x, time_series_price, color='black')

            # ax2 (right Y axis)
            # ax_ind.set_ylabel("ATR", color='tab:blue', fontsize=20)
            self.ax_indicator.tick_params(axis='y', labelcolor='tab:green')
            # ax_ind.set_title("ATR", fontsize=22)
            self.ax_indicator.grid(alpha=.4)
            self.ax_indicator.spines["top"].set_alpha(0.0)
            self.ax_indicator.spines["bottom"].set_alpha(1)
            self.ax_indicator.spines["right"].set_alpha(0.0)
            self.ax_indicator.spines["left"].set_alpha(1)

        else: # here goes code for bolinger bands i.e
            pass





    # this has to be called after calling plot_main
    def plot_indicator(self, df, period=100):

        title = "{}".format(self.ticker)

        indicator_key = df.columns[0]


        x = df.iloc[:, [0]]
        x = x.iloc[-period:, :].index
        time_series_indicator = df.iloc[-period:, :][indicator_key]

        if self.fig is None or self.ax_indicator is None:
            print("Please call first method plot_main")

        self.ax_indicator.set_ylabel(indicator_key, color='tab:green', fontsize=20)
        # Plot Line2 (Right Y Axis)
        self.ax_indicator.plot(x, time_series_indicator, color='tab:green')

        self.fig.tight_layout()

        self.ax_indicator1 = self.ax_indicator.twinx()  # instantiate a second axes that shares the same x-axis
        self.ax_indicator2 = self.ax_indicator1.twinx()  # instantiate a second axes that shares the same x-axis

        self.ax_indicator1.plot(x, time_series_indicator, color='tab:green')

        self.ax_indicator2.plot(x, time_series_indicator, color='tab:red')



        self.fig.canvas.draw()

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
