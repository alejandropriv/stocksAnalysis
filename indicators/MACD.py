class MACD:

    ### price is Dataframew
    def __init__(self, price, fast_period=12, slow_period=26, signal_period=9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

        self.price = price

    def calculate(self):
        """function to calculate MACD
           typical values a = 12; b =26, c =9"""

        print("MACD added for: {}".format(self.price))

        df_macd = self.price.iloc[:, [0]].copy()
        ticker = self.price.columns[0]

        fast_key = "{}_{}".format(ticker, "MA_Fast")
        slow_key = "{}_{}".format(ticker, "MA_Slow")
        macd_key = "{}_{}".format(ticker, "MACD")
        signal_key = "{}_{}".format(ticker, "Signal")

        df_macd[fast_key] = df_macd[ticker].ewm(span=self.fast_period,
                                                min_periods=self.fast_period).mean()

        df_macd[slow_key] = df_macd[ticker].ewm(span=self.slow_period,
                                                min_periods=self.slow_period).mean()

        df_macd[macd_key] = df_macd[fast_key] - df_macd[slow_key]

        df_macd[signal_key] = df_macd[macd_key].ewm(span=self.signal_period,
                                                    min_periods=self.signal_period).mean()


        df_macd.drop(columns=fast_key, inplace=True)
        df_macd.drop(columns=slow_key, inplace=True)


        df_macd.dropna(inplace=True)  # TODO: check if no extra data is lost in each iteration

        return df_macd
