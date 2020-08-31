from utilities.Constants import Constants
from indicators.Indicator import Indicator
import pandas as pd
import copy



class MACD(Indicator):

    # price is DataFrame, = adj_close
    def __init__(self, df=None, fast_period=12, slow_period=26, signal_period=9):
        super().__init__()


        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

        # Set dataframe keys
        self.adj_close_key = None
        self.close_key = None

        self.macd_key = None
        self.signal_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)

        # Set dataFrame keys
        adj_close_key = Constants.get_adj_close_key()
        close_key = Constants.get_close_key()

        self.macd_key = Constants.get_key("MACD")
        self.signal_key = Constants.get_key("Signal")


        if adj_close_key in df.columns is True:
            for ticker in self.tickers:
                temp = pd.DataFrame(df[ticker][adj_close_key].copy())
                self.df = pd.concat([temp], axis=1, keys=[ticker, adj_close_key])

            self.adj_close_key = adj_close_key

        else:

            self.adj_close_key = close_key

            prices_temp = pd.DataFrame()

            df_list = []
            for ticker in self.tickers:
                df_list.append(pd.concat([df[ticker].loc[:, [self.adj_close_key]], prices_temp], axis=1, keys=[ticker]))

            df_indicator = pd.concat(
                df_list,
                axis=1
            )

            self.df = copy.copy(df_indicator)





    def calculate(self):
        """function to calculate MACD
           typical values a = 12; b =26, c =9"""

        if self.df is None:
            print("Error Constructing the Indicator, Please verify constructor")
            raise ValueError

        # Set temp dataframe keys
        fast_key = Constants.get_key("MA_Fast")
        slow_key = Constants.get_key("MA_Slow")

        df_data = pd.DataFrame()

        for ticker in self.tickers:
            df_data = self.df[ticker].copy()

            df_data[fast_key] = \
                df_data[self.adj_close_key].ewm(
                    span=self.fast_period,
                    min_periods=self.fast_period
                ).mean()

            df_data[slow_key] = \
                df_data[self.adj_close_key].ewm(
                    span=self.slow_period,
                    min_periods=self.slow_period
                ).mean()

            df_data[self.macd_key] = \
                df_data[fast_key] - df_data[slow_key]

            df_data[self.signal_key] = \
                df_data[self.macd_key].ewm(
                    span=self.signal_period,
                    min_periods=self.signal_period
                ).mean()

            df_data.drop(columns=[fast_key, slow_key], inplace=True)

            df_data.dropna(inplace=True)

        self.df = df_data.copy()

        return self.df



    def plot(self, plotter=None, period=100, color="tab:green"):

        super().plot(plotter=plotter, period=period, color=color)

        print("Plotting MACD")

        max_value = self.df[self.macd_key].max()
        min_value = self.df[self.macd_key].min()

        if plotter.ax_indicators is None or len(plotter.ax_indicators) <= 1:
            plotter.ax_indicators[self.macd_key] = plotter.ax_indicators[Constants.main_indicator_axis]

        else:
            # instantiate a second axes that shares the same x-axis
            plotter.ax_indicators[self.macd_key] = \
                plotter.ax_indicators[Constants.main_indicator_axis].twinx()


        plotter.ax_indicators[self.macd_key].set_ylim(min_value - 1, max_value + 1)

        plotter.main_ax_indicator = plotter.ax_indicators[self.macd_key]
        plotter.main_ax_indicator.tick_params(axis='y', labelcolor=color, size=20)
        plotter.plot_indicator(df=self.df[[self.macd_key]], period=period, color=color)
        plotter.plot_indicator(df=self.df[[self.signal_key]], period=period, color="tab:orange")

        legend_position = plotter.get_legend_position()
        plotter.ax_indicators[self.macd_key].legend(loc=legend_position)

        return plotter




