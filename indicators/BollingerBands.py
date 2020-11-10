from utilities.Constants import Constants
from indicators.Indicator import Indicator
import pandas as pd




class BollingerBands(Indicator):

    # price is Dataframe
    def __init__(self, df=None, n=20):
        super().__init__()

        self.in_main_plot = True
        self.n = n

        # Set dataframe keys
        self.prices_key = None
        self.bb_up_key = None
        self.bb_down_key = None
        self.bb_width_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataFrame keys
        self.bb_up_key = Constants.get_key("BB_up")
        self.bb_down_key = Constants.get_key("BB_down")
        self.bb_width_key = Constants.get_key("BB_width")

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
        """function to calculate Bollinger Bands"""

        super().calculate()

        # Set temp dataframe keys
        ma_key = Constants.get_key("MA")

        df_data = pd.DataFrame()
        df_result = []

        for ticker in self.tickers:
            df_data = self.df[ticker].copy()

            #df_data.rename(columns={self.ticker: self.prices_key}, inplace=True) #TODO: what happens with this

            df_data[ma_key] = \
                df_data[self.prices_key].rolling(self.n).mean()

            # ddof=0 is required since we want to take the standard deviation of the population and not sample
            df_data[self.bb_up_key] = \
                df_data[ma_key] + 2 * df_data[self.prices_key].rolling(self.n).std(ddof=0)

            # ddof=0 is required since we want to take the standard deviation of the population and not sample
            df_data[self.bb_down_key] = \
                df_data[ma_key] - 2 * df_data[self.prices_key].rolling(self.n).std(ddof=0)
            df_data[self.bb_width_key] = df_data[self.bb_up_key] - df_data[self.bb_down_key]
            df_data.dropna(inplace=True)

            df_result.append(df_data.loc[:, [self.bb_up_key, self.bb_down_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)

        return df_data
