from utilities.Constants import Constants
from indicators.Indicator import Indicator
import pandas as pd



class ATR(Indicator):

    # price is Dataframe
    def __init__(self, df=None, n=14):
        super().__init__()

        self.n = n

        # Set dataframe keys
        self.low_key = None
        self.high_key = None
        self.adj_close_key = None
        self.indicator_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataframe keys
        self.low_key = Constants.get_low_key()
        self.high_key = Constants.get_high_key()
        self.adj_close_key = Constants.get_adj_close_key()
        adj_close_key = Constants.get_adj_close_key()
        close_key = Constants.get_close_key()

        self.indicator_key = Constants.get_key("ATR")


        if adj_close_key in df.columns is True:
            self.adj_close_key = adj_close_key

        else:
            self.adj_close_key = close_key


        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:

            df_list.append(
                pd.concat(
                    [df[ticker].loc[:, [self.low_key, self.high_key, self.adj_close_key]], prices_temp],
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
        """function to calculate True Range and Average True Range"""

        if self.df is None:
            print("DF has not been set, there is no data to calculate the indicator, "
                  "please verify the indicator constructor")
            raise ValueError

        # Set temp dataframe keys
        h_l_key = Constants.get_key("H-L")
        h_pc_key = Constants.get_key("H-PC")
        l_pc_key = Constants.get_key("L-PC")
        tr_key = Constants.get_key("TR")

        df_data = pd.DataFrame()
        df_result = []

        for ticker in self.tickers:
            df_data = self.df[ticker].copy()
            df_data[h_l_key] = abs(df_data[self.high_key] - df_data[self.low_key])
            df_data[h_pc_key] = abs(df_data[self.high_key] - df_data[self.adj_close_key].shift(1))
            df_data[l_pc_key] = abs(df_data[self.low_key] - df_data[self.adj_close_key].shift(1))
            df_data[tr_key] = df_data[[h_l_key, h_pc_key, l_pc_key]].max(axis=1, skipna=False)
            df_data[self.indicator_key] = df_data[tr_key].rolling(self.n).mean()
            # df[indicator_key] = df[tr_key].ewm(span=n,adjust=False,min_periods=n).mean()
            # df_data.dropna(inplace=True, axis=0)

            df_data.drop([h_l_key, h_pc_key, l_pc_key], axis=1, inplace=True)

            df_result.append(df_data.loc[:, [self.indicator_key, tr_key]])

        self.df = pd.concat(df_result, axis=1, keys=self.tickers)


        return self.df


    # # expect Stock, volume, Indicator
    # def plot(self, plotter=None, period=100, color="tab:red"):
    #
    #     super().plot(plotter=plotter, period=period, color=color)
    #
    #     self.plot_indicator(
    #         plotter=plotter,
    #         period=period,
    #         key=self.indicator_key,
    #         color=color,
    #         legend_position=None
    #     )
