from utilities.Constants import Constants
from indicators.Indicator import Indicator
from indicators.ATR import ATR

import pandas as pd


from stocktrends import Renko


class RENKOIND(Indicator):
    def __init__(self, df=None, n=120):
        super().__init__()
        self.collapse = False

        self.n = n

        # Set dataframe keys
        self.low_key = None
        self.high_key = None
        self.open_key = None
        self.date_key = "Date"

        self.prices_key = None

        self.brick_size = None

        self.df_renko_input = None
        self.df_renko = None
        self.renko_data = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        self.low_key = Constants.get_low_key()
        self.high_key = Constants.get_high_key()
        self.open_key = Constants.get_open_key()

        # Set dataframe keys
        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:
            df_temp = df[ticker].loc[:, [self.high_key, self.low_key, self.open_key, self.prices_key]]

            df_list.append(
                pd.concat(
                    [df_temp, prices_temp],
                    axis=1,
                    keys=[ticker]
                )
            )

        df_indicator = pd.concat(
            df_list,
            axis=1
        )

        self.df = df_indicator.copy()


        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:
            df_temp = df[ticker]
            df_temp.reset_index(level=0, inplace=True)
            df_temp = df_temp.loc[:, [self.date_key, self.high_key, self.low_key, self.open_key, self.prices_key]] # TODO: Is this rebundant???

            df_temp.rename(
                columns={
                    "Date": "date",
                    self.high_key: "high",
                    self.low_key: "low",
                    self.open_key: "open",
                    self.prices_key: "close"},
                inplace=True)

            df_list.append(
                pd.concat(
                    [df_temp, prices_temp],
                    axis=1,
                    keys=[ticker]
                )
            )

        df_indicator = pd.concat(
            df_list,
            axis=1
        )

        self.df_renko_input = df_indicator.copy()




    def calculate(self):
        """function to convert ohlc data into renko bricks"""

        super().calculate()

        df_result = []

        for ticker in self.tickers:

            df_data_atr = self.df[[ticker]].copy()
            atr = ATR(df_data_atr, 120)
            df_atr = atr.calculate()


            df_data = self.df_renko_input[ticker].copy()

            self.df_renko = Renko(df_data)

            atr_key = Constants.get_key("ATR")


            self.df_renko.brick_size = round(df_atr[ticker][atr_key][-1], 0)
            self.brick_size = self.df_renko.brick_size

            # renko_df = df2.get_bricks() #if get_bricks() does not work try using get_ohlc_data() instead
            self.renko_data = self.df_renko.get_ohlc_data()
            df_result.append(self.renko_data)

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return self.df








