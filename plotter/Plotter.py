import matplotlib.pyplot as plt


class Plotter:


    @staticmethod
    def plot_prices_close_adj(prices):
        # Data visualization
        prices.plot()  # Plot of all the stocks superimposed on the same chart


    @staticmethod
    def plot_standard(prices):
        # Standardization
        cp_standardized = \
            (prices - prices.mean()) / prices.std()

        cp_standardized.plot()  # Plot of all the stocks standardized and superimposed on the same chart


    @staticmethod
    def plot_comparative(prices, title, y, x):
        prices.plot(subplots=True, layout=(y, x), title=title,  # TODO: stock.title? stock.meta.title?
                    grid=True)  # Subplots of the stocks


    # expect Stock, volume, Indicator
    @staticmethod
    def plot_macd(df, period=100,  title=""):  # TODO: this is not correct

        title = "{} {}".format(title, df.columns[0])


        x = df.iloc[:, [0]]
        x = x.iloc[-period:, :].index
        time_series_price = df.iloc[-period:, 0]
        time_series_macd = df.iloc[-period:, 1]
        time_series_signal = df.iloc[-period:, 2]
        time_series_volume = df.iloc[-period:, 3]


        # Plot Line1 (Left Y Axis)
        fig, (ax_vol, ax_macd) = plt.subplots(2, 1, figsize=(16, 9), dpi=80, sharex=True, gridspec_kw={'height_ratios': [3, 1]})

        ax_vol.set_ylim(0, 100000000)
        ax_vol.bar(x, time_series_volume, color='tab:blue', alpha=0.5)
        ax_vol.tick_params(axis='y', rotation=0, labelcolor='tab:blue')

        ax_pri = ax_vol.twinx()  # instantiate a second axes that shares the same x-axis

        ax_pri.plot(x, time_series_price, color='tab:red')



        # Plot Line2 (Right Y Axis)
        ax_macd.plot(x, time_series_macd, color='tab:orange')
        ax_macd.plot(x, time_series_signal, color='tab:green')


        # Decorations
        # ax1 (left Y axis)
        ax_pri.set_title(title, fontsize=22)
        ax_pri.tick_params(axis='x', rotation=0, labelsize=12, labelleft=True)
        ax_pri.set_ylabel('Price', color='tab:red', fontsize=20)
        ax_pri.tick_params(axis='y', rotation=0, labelcolor='tab:red')
        ax_pri.grid(alpha=.4)

        ax_pri.spines["top"].set_alpha(0.0)
        ax_pri.spines["bottom"].set_alpha(1)
        ax_pri.spines["right"].set_alpha(0.0)
        ax_pri.spines["left"].set_alpha(1)
        ax_vol.spines["top"].set_alpha(0.0)
        ax_vol.spines["bottom"].set_alpha(1)
        ax_vol.spines["right"].set_alpha(0.0)
        ax_vol.spines["left"].set_alpha(1)

        # ax2 (right Y axis)
        ax_macd.set_ylabel("MACD/Signal", color='tab:blue', fontsize=20)
        ax_macd.tick_params(axis='y', labelcolor='tab:blue')
        ax_macd.set_title("MACD", fontsize=22)
        ax_macd.grid(alpha=.4)
        ax_macd.spines["top"].set_alpha(0.0)
        ax_macd.spines["bottom"].set_alpha(1)
        ax_macd.spines["right"].set_alpha(0.0)
        ax_macd.spines["left"].set_alpha(1)

        ax_macd.legend(title='')

        fig.tight_layout()
        plt.show()



    @staticmethod
    def plot_bollinger_bands(df, period=100,  title=""):  # TODO: this is not correct

        title = "{} {}".format(title, "MACD")

        x = df.loc[:, ["FB"]]
        x = x.iloc[-period:, :].index
        y1 = df.iloc[-period:, 1]
        y2 = df.iloc[-period:, 4]

        # Plot Line1 (Left Y Axis)
        fig, ax1 = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
        ax1.plot(x, y1, color='tab:red')

        # Plot Line2 (Right Y Axis)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.plot(x, y2, color='tab:blue')

        # Decorations
        # ax1 (left Y axis)
        ax1.set_xlabel('Date', fontsize=20)
        ax1.tick_params(axis='x', rotation=0, labelsize=12)
        ax1.set_ylabel('Stock', color='tab:red', fontsize=20)
        ax1.tick_params(axis='y', rotation=0, labelcolor='tab:red')
        ax1.grid(alpha=.4)

        # ax2 (right Y axis)
        ax2.set_ylabel("MACD", color='tab:blue', fontsize=20)
        ax2.tick_params(axis='y', labelcolor='tab:blue')
        # ax2.set_xticks(np.arange(0, len(x), 60))
        # ax2.set_xticklabels(x[::60], rotation=90, fontdict={'fontsize': 10})
        ax2.set_title("MACDAX2", fontsize=22)
        fig.tight_layout()
        plt.show()
