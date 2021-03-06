from utilities.Constants import Constants
import numpy as np
from indicators.Indicator import Indicator
import pandas as pd



class RSI(Indicator):

    # price is Dataframe
    def __init__(self, df=None, n=14):
        super().__init__()

        self.n = n

        # Set dataframe keys
        self.prices_key = None
        self.indicator_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataframe keys
        self.indicator_key = Constants.get_key("RSI")

        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:
            if ticker in df:
                df_list.append(
                    pd.concat(
                        [df[ticker].loc[:, [self.prices_key]], prices_temp],
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
        """function to calculate RSI
           typical values n=14"""

        super().calculate()

        delta_key = Constants.get_key("delta")
        gain_key = Constants.get_key("gain")
        loss_key = Constants.get_key("loss")
        avg_gain_key = Constants.get_key("avg_gain")
        avg_loss_key = Constants.get_key("avg_loss")
        rs_key = Constants.get_key("RS")

        df_result = []

        for ticker in self.tickers:

            df_data = self.df[ticker].copy()

            df_data[delta_key] = df_data[self.prices_key] - df_data[self.prices_key].shift(1)
            df_data[gain_key] = np.where(df_data[delta_key] >= 0, df_data[delta_key], 0)
            df_data[loss_key] = np.where(df_data[delta_key] < 0, abs(df_data[delta_key]), 0)
            avg_gain = []
            avg_loss = []
            gain = df_data[gain_key].tolist()
            loss = df_data[loss_key].tolist()

            for i in range(len(df_data)):
                if i < self.n:
                    avg_gain.append(np.NaN)
                    avg_loss.append(np.NaN)
                elif i == self.n:
                    avg_gain.append(df_data[gain_key].rolling(self.n).mean().tolist()[self.n])
                    avg_loss.append(df_data[loss_key].rolling(self.n).mean().tolist()[self.n])
                elif i > self.n:
                    avg_gain.append(((self.n - 1) * avg_gain[i - 1] + gain[i]) / self.n)
                    avg_loss.append(((self.n - 1) * avg_loss[i - 1] + loss[i]) / self.n)


            df_data[avg_gain_key] = np.array(avg_gain)
            df_data[avg_loss_key] = np.array(avg_loss)
            df_data[rs_key] = df_data[avg_gain_key] / df_data[avg_loss_key]
            df_data[self.indicator_key] = 100 - (100 / (1 + df_data[rs_key]))

            df_result.append(df_data.loc[:, [self.indicator_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return self.df


