from utilities.Constants import Constants
from indicators.Indicator import Indicator
from indicators.ATR import ATR

from stocktrends import Renko
from stocktrends import indicators

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt


class RENKOIND(Indicator):
    def __init__(self, df=None, n=120):
        super().__init__()

        self.n = n

        # Set dataframe keys
        self.low_key = None
        self.high_key = None
        self.open_key = None
        self.close_key = None
        self.adj_close_key = None

        self.brick_size = None

        self.df_renko = None

        if df is not None:
            self.set_input_data(df)

    def set_input_data(self, df):
        super().set_input_data(df)

        self.low_key = Constants.get_low_key(self.ticker)
        self.high_key = Constants.get_high_key(self.ticker)
        self.open_key = Constants.get_open_key(self.ticker)
        self.close_key = Constants.get_close_key(self.ticker)
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)


        self.df = df.copy()
        self.df.reset_index(inplace=True)

        self.df_renko = df.loc[:, [self.high_key, self.low_key, self.open_key, self.adj_close_key]]

        self.df_renko.rename(
            columns={
                "Date": "date",
                self.high_key: "high",
                self.low_key: "low",
                self.open_key: "open",
                self.adj_close_key: "close"}, inplace=True)



        # Set dataframe keys
        self.df.ticker = df.ticker
        self.df_renko.ticker = df.ticker


    def calculate(self):
        """function to convert ohlc data into renko bricks"""

        df2 = Renko(self.df_renko)
        df2.brick_size = round(ATR(self.df, 120)["ATR"][-1], 0)
        self.brick_size = df2.brick_size

        # renko_df = df2.get_bricks() #if get_bricks() does not work try using get_ohlc_data() instead
        renko_df = df2.get_ohlc_data()
        self.df = renko_df.copy()
        return self.df


        # expect Stock, volume, Indicator
    def plot(self, plotter=None, period=100, color="tab:green"):

        self.df.columns = [i.lower() for i in self.df.columns]
        rows = period

        renko = indicators.Renko(self.df)

#        print('\n\nRenko box calculation based on periodic close')
#        renko.brick_size = 2
#        renko.chart_type = indicators.Renko.PERIOD_CLOSE
#        data = renko.get_ohlc_data()
#        print(data.tail(rows))

        print('\n\nRenko box calculation based on price movement')
        renko.chart_type = indicators.Renko.PRICE_MOVEMENT
        data = renko.get_ohlc_data()
        print(data.tail(rows))

        data = data.copy()
        data['cdiff'] = data['close'] - data['close'].shift(1)
        data.dropna(inplace=True)
        data['bricks'] = data.loc[:, ('cdiff',)] / self.brick_size

        bricks = data[data['bricks'] != 0]['bricks'].values


        self.plot_renko(self, bricks)





    def plot_renko(self, data):
        fig = plt.figure(1)
        fig.clf()
        axes = fig.gca()
        y_max = max(data)

        prev_num = 0

        bricks = []

        for delta in data:
            if delta > 0:
                bricks.extend([1] * delta)
            else:
                bricks.extend([-1] * abs(delta))

        for index, number in enumerate(bricks):
            if number == 1:
                facecolor = 'green'
            else:
                facecolor = 'red'

            prev_num += number

            renko = Rectangle(
                (index, prev_num * self.brick_size), 1, self.brick_size,
                facecolor=facecolor, alpha=0.5
            )
            axes.add_patch(renko)

        plt.show()




