from utilities.Constants import Constants
from indicators.Indicator import Indicator
from indicators.ATR import ATR

from stocktrends import Renko

import matplotlib.patches as ppatches
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
        self.date_key = "Date"

        self.brick_size = None

        self.df_t = None
        self.df_renko = None
        self.renko_data = None

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
        self.df_t = df.copy()
        self.df_t.reset_index(inplace=True)

        self.df_t = self.df_t.loc[:, [self.date_key, self.high_key, self.low_key, self.open_key, self.adj_close_key]]

        self.df_t.rename(
            columns={
                "Date": "date",
                self.high_key: "high",
                self.low_key: "low",
                self.open_key: "open",
                self.adj_close_key: "close"}, inplace=True)



        # Set dataframe keys
        self.df.ticker = df.ticker
        self.df_t.ticker = df.ticker


    def calculate(self):
        """function to convert ohlc data into renko bricks"""

        self.df_renko = Renko(self.df_t)
        self.df_renko.ticker = self.df_t.ticker


        atr = ATR(self.df, 120)
        df_atr = atr.calculate()

        atr_key = Constants.get_key(self.ticker, "ATR")


        self.df_renko.brick_size = round(df_atr[atr_key][-1], 0)
        self.brick_size = self.df_renko.brick_size


        # renko_df = df2.get_bricks() #if get_bricks() does not work try using get_ohlc_data() instead
        self.renko_data = self.df_renko.get_ohlc_data()
        self.df = self.renko_data.copy()
        return self.df # TODO: Check that this format is consistent through all the indicators


        # expect Stock, volume, Indicator
    def plot(self, plotter=None, period=100, color="tab:green"):


        self.plot_renko(self.renko_data, self.brick_size)




    #TODO. This is working partially
    def plot_renko(self, data, brick_size):

        lim_y_min = min(data.loc[:, "close"]) - 100
        lim_y_max = max(data.loc[:, "close"]) + 100


        prev_num = -1
        y0 = data.loc[0, "close"]

        uptrend = data.loc[:, ["uptrend"]]
        fig = plt.figure(2)
        fig.clf()
        axes = fig.gca()




        bricks = []

        for index, delta in uptrend.iterrows():
            if delta.loc["uptrend"] == True:
                bricks.extend([1] * 1)
            else:
                bricks.extend([-1] * 1)


        for index, number in enumerate(bricks):
            if number == 1:
                facecolor = 'green'
            else:
                facecolor = 'red'

            prev_num += number



            renko = ppatches.Rectangle(
                (index, prev_num * self.brick_size + y0), 1, self.brick_size,
                facecolor=facecolor, alpha=0.5
            )
            axes.add_patch(renko)


            print ("x: {} y:{}, width:{}, height:{} ".format(
                index, prev_num * brick_size, 1, brick_size)
            )


        plt.xticks()
        axes.set_xlim(0, 100)
        axes.set_ylim(lim_y_min, lim_y_max)

        #plt.show()




