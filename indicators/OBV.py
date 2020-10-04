from utilities.Constants import Constants
import numpy as np
import pandas as pd


from indicators.Indicator import Indicator



class OBV(Indicator):
    #TODO verify the correct data is present
    # df requires:  price adjusted close
    #               volume
    def __init__(self, df=None, n=14):
        super().__init__()

        self.n = n

        # Set dataframe keys
        self.volume_key = None
        self.indicator_key = None
        self.prices_key = None

        if df is not None:
            self.set_input_data(df)



    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataFrame keys
        self.volume_key = Constants.get_volume_key()
        self.indicator_key = Constants.get_key("OBV")


        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:
            df_list.append(
                pd.concat(
                    [df[ticker].loc[:, [self.volume_key, self.prices_key]], prices_temp],
                    axis=1,
                    keys=[ticker]
                )
            )

        df_indicator = pd.concat(
            df_list,
            axis=1
        )

        self.df = df_indicator.copy()



    def calculate(self):
        """function to calculate On Balance Volume"""

        if self.df is None:
            print("DF has not been set, there is no data to calculate the indicator, "
                  "please verify the indicator constructor")
            raise ValueError

        daily_ret_key = Constants.get_key("daily_ret")
        direction_key = Constants.get_key("direction")
        volume_adjusted_key = Constants.get_key("vol_adj")

        df_result = []

        for ticker in self.tickers:

            df_data = self.df[ticker].copy()

            df_data[daily_ret_key] = df_data[self.prices_key].pct_change()
            df_data[direction_key] = np.where(df_data[daily_ret_key] >= 0, 1, -1)
            #df_data.loc[0, direction_key] = 0
            df_data.iloc[0].at[direction_key] = 0
            #df_data[direction_key][0] = 0 #TODO check this for copy vs
            df_data[volume_adjusted_key] = df_data[self.volume_key] * df_data[direction_key]
            df_data[self.indicator_key] = df_data[volume_adjusted_key].cumsum()

            df_result.append(df_data.loc[:, [self.indicator_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return self.df
