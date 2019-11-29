import matplotlib.pyplot as plt


class MACD:

    def __init__(self, price, fast_period=12, slow_period=26, signal_period=9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

        self.price = price

        self.df_ma = self.price.copy()

    def calculate(self):
        """function to calculate MACD
           typical values a = 12; b =26, c =9"""

        for price in self.price:
            print("MACD added for: {}".format(price))

            fast_key = "{}_{}".format(price, "MA_Fast")
            slow_key = "{}_{}".format(price, "MA_Slow")
            macd_key = "{}_{}".format(price, "MACD")
            signal_key = "{}_{}".format(price, "Signal")

            self.df_ma[fast_key] = self.df_ma[price].ewm(span=self.fast_period,
                                                         min_periods=self.fast_period).mean()
            self.df_ma[slow_key] = self.df_ma[price].ewm(span=self.slow_period,
                                                         min_periods=self.slow_period).mean()
            self.df_ma[macd_key] = self.df_ma[fast_key] - self.df_ma[slow_key]
            self.df_ma[signal_key] = self.df_ma[macd_key].ewm(span=self.signal_period,
                                                              min_periods=self.signal_period).mean()

            self.df_ma.dropna(inplace=True)




    def plot(self, period=100):  # TODO: this is not correct

        for price in self.price:

            # Visualization - plotting MACD/signal along with close price and volume for last 100 data points
            plt.subplot(311)
            plt.plot(self.df_ma.loc[price])
            plt.title('MSFT Stock Price')
            plt.xticks([])

            plt.subplot(312)
            plt.bar(self.df_ma.iloc[-period:, 5].index, self.df_ma.iloc[-period:, 5].values)
            plt.title('Volume')
            plt.xticks([])

            plt.subplot(313)
            plt.plot(self.df_ma.iloc[-period:, [-2, -1]])
            plt.title('MACD')
            plt.legend(('MACD', 'Signal'), loc='lower right')

            plt.show()

            # Visualization - Using object orient approach
            # Get the figure and the axes
            fig, (ax0, ax1) = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False, figsize=(10, 6),
                                           gridspec_kw={'height_ratios': [2.5, 1]})
            self.df_ma.iloc[-100:, 4].plot(ax=ax0)
            ax0.set(ylabel='Adj Close')

            self.df_ma.iloc[-100:, [-2, -1]].plot(ax=ax1)
            ax1.set(xlabel='Date', ylabel='MACD/Signal')

            # Title the figure
            fig.suptitle('Stock Price with MACD', fontsize=14, fontweight='bold')
