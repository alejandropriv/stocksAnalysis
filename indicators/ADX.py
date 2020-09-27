from utilities.Constants import Constants
import numpy as np
from indicators.ATR import ATR
from indicators.Indicator import Indicator
import pandas as pd




class ADX(Indicator):

    # price is Dataframe
    def __init__(self, df=None, n=14):

        super().__init__()

        self.n = n

        # Set dataframe keys
        self.low_key = None
        self.high_key = None
        self.prices_key = None
        self.indicator_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataFrame keys
        adj_close_key = Constants.get_adj_close_key()
        close_key = Constants.get_close_key()

        if adj_close_key in df.columns is True:
            self.prices_key = adj_close_key

        else:
            self.prices_key = close_key

        self.low_key = Constants.get_low_key()
        self.high_key = Constants.get_high_key()
        self.indicator_key = Constants.get_key("ADX")

        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:
            df_list.append(
                pd.concat(
                    [df[ticker].loc[:, [self.low_key, self.high_key, self.prices_key]], prices_temp],
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
        """"function to calculate ADX"""

        if self.df is None:
            print("DF has not been set, there is no data to calculate the indicator, "
                  "please verify the indicator constructor")
            raise ValueError


        tr_key = Constants.get_key("TR")
        trn_key = Constants.get_key("TRn")

        dm_plus_key = Constants.get_key("DMplus")
        dm_plus_n_key = Constants.get_key("DMplusN")

        dm_minus_key = Constants.get_key("DMminus")
        dm_minus_n_key = Constants.get_key("DMminusN")
        di_plus_n_key = Constants.get_key("DIplusN")
        di_minus_n_key = Constants.get_key("DIminusN")
        di_diff_key = Constants.get_key("DIdiff")
        di_sum_key = Constants.get_key("DIsum")
        dx_key = Constants.get_key("DX")

        df_result = []

        for ticker in self.tickers:

            df_data_atr = self.df[[ticker]].copy()
            atr_ind = ATR(df=df_data_atr, n=14)

            df_data = self.df[ticker].copy()
            # the period parameter of ATR function does not matter because period does not influence TR calculation
            df_data[tr_key] = atr_ind.calculate()[ticker][[tr_key]]

            df_data[dm_plus_key] = \
                np.where(
                    (df_data[self.high_key] - df_data[self.high_key].shift(1)) >
                    (df_data[self.low_key].shift(1) - df_data[self.low_key]),
                    df_data[self.high_key] - df_data[self.high_key].shift(1),
                    0)

            df_data[dm_plus_key] = \
                np.where(
                    df_data[dm_plus_key] < 0,
                    0,
                    df_data[dm_plus_key])

            df_data[dm_minus_key] = \
                np.where((df_data[self.low_key].shift(1) - df_data[self.low_key]) >
                         (df_data[self.high_key] - df_data[self.high_key].shift(1)),
                         df_data[self.low_key].shift(1) - df_data[self.low_key],
                         0)

            df_data[dm_minus_key] = np.where(df_data[dm_minus_key] < 0, 0, df_data[dm_minus_key])

            TRn = []
            DMplusN = []
            DMminusN = []
            TR = df_data[tr_key].tolist()
            DMplus = df_data[dm_plus_key].tolist()
            DMminus = df_data[dm_minus_key].tolist()

            for i in range(len(df_data)):
                if i < self.n:
                    TRn.append(np.NaN)
                    DMplusN.append(np.NaN)
                    DMminusN.append(np.NaN)
                elif i == self.n:
                    TRn.append(df_data[tr_key].rolling(self.n).sum().tolist()[self.n])
                    DMplusN.append(df_data[dm_plus_key].rolling(self.n).sum().tolist()[self.n])
                    DMminusN.append(df_data[dm_minus_key].rolling(self.n).sum().tolist()[self.n])
                elif i > self.n:
                    TRn.append(TRn[i - 1] - (TRn[i - 1] / 14) + TR[i])
                    DMplusN.append(DMplusN[i - 1] - (DMplusN[i - 1] / 14) + DMplus[i])
                    DMminusN.append(DMminusN[i - 1] - (DMminusN[i - 1] / 14) + DMminus[i])

            df_data[trn_key] = np.array(TRn)
            df_data[dm_plus_n_key] = np.array(DMplusN)
            df_data[dm_minus_n_key] = np.array(DMminusN)
            df_data[di_plus_n_key] = 100 * (df_data[dm_plus_n_key] / df_data[trn_key])
            df_data[di_minus_n_key] = 100 * (df_data[dm_minus_n_key] / df_data[trn_key])
            df_data[di_diff_key] = abs(df_data[di_plus_n_key] - df_data[di_minus_n_key])
            df_data[di_sum_key] = df_data[di_plus_n_key] + df_data[di_minus_n_key]
            df_data[dx_key] = 100 * (df_data[di_diff_key] / df_data[di_sum_key])
            ADX = []
            DX = df_data[dx_key].tolist()
            for j in range(len(df_data)):
                if j < 2 * self.n - 1:
                    ADX.append(np.NaN)
                elif j == 2 * self.n - 1:
                    ADX.append(df_data[dx_key][j - self.n + 1:j + 1].mean())
                elif j > 2 * self.n - 1:
                    ADX.append(((self.n - 1) * ADX[j - 1] + DX[j]) / self.n)
            df_data[self.indicator_key] = np.array(ADX)

            df_result.append(df_data.loc[:, [self.indicator_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return self.df
