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

        super().plot(plotter=plotter, period=period, color=color)

        self.plot_indicator(
            plotter=plotter,
            period=period,
            key="RENKO",
            color=color,
            legend_position=None
        )

        #self.plot_renko(self.renko_data, self.brick_size)


    def plot_indicator(self, plotter=None, period=100, key=None, color="tab:green", legend_position=None):

        if plotter is None:
            print("Error: plotter Object not found, please Select the main stock first.")
            return

        if legend_position is None:
            legend_position = plotter.get_legend_position()

        print("Plotting {}".format(key))

        key_close = "close"
        uptrend_key = "uptrend"
        date_key = "date"

        lim_y_min = min(self.df.loc[:, key_close]) - 100
        lim_y_max = max(self.df.loc[:,key_close]) + 100


        prev_num = -1
        y0 = self.df.loc[0, key_close]

        uptrend = self.df.loc[:, [uptrend_key]]
        date = self.df.loc[:,date_key]




        bricks = []

        for index, delta in uptrend.iterrows():
            if delta.loc["uptrend"] == True:
                bricks.extend([1] * 1)
            else:
                bricks.extend([-1] * 1)

        if plotter.ax_indicators is None or len(plotter.ax_indicators) <= 1:
            print("This is the first indicator, in the plot")
            plotter.ax_indicators[key] = plotter.ax_indicators[Constants.main_indicator_axis]

        else:
            print("This indicator is added to the current-existing plot")
            # instantiate a second axes that shares the same x-axis
            plotter.ax_indicators[key] = plotter.ax_indicators[Constants.main_indicator_axis].twinx()


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
            plotter.ax_indicators[key].add_patch(renko)




        plotter.ax_indicators[key].set_ylim(lim_y_min, lim_y_max)

        plotter.main_ax_indicator = plotter.ax_indicators[key]
        plotter.main_ax_indicator.tick_params(axis='y', labelcolor=color, size=20)


        plotter.ax_indicators[key].legend(loc=legend_position)

        #plt.xticks(range(date.count()), date, rotation=90)
        # Use the pyplot interface to change just one subplot...
        plt.sca(plotter.ax_indicators[key])
        plt.xticks(range(date.count()),  date.apply(str), rotation=90)

        lim_x_min = 0
        lim_x_max = date.count()

        plotter.ax_indicators[key].set_xlim(lim_x_min, lim_x_max)

        plotter.ax_indicators[key].legend(["RENKO"])


    def plot_renko(self, data, brick_size):

        lim_y_min = min(data.loc[:, "close"]) - 100
        lim_y_max = max(data.loc[:, "close"]) + 100


        prev_num = -1
        y0 = data.loc[0, "close"]

        uptrend = data.loc[:, ["uptrend"]]
        date = data.loc[:, "date"]


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

        plt.xticks(range(date.count()), date, rotation=90)
        axes.set_ylim(lim_y_min, lim_y_max)

        lim_x_min = 0
        lim_x_max = date.count()

        axes.set_xlim(lim_x_min, lim_x_max)


        #plt.show()




