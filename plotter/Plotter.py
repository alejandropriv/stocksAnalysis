import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from indicators.MACD import MACD
from indicators.ATR import ATR

from plotter.PlotterIndicator import PlotterIndicator
from plotter.PlotterMACD import PlotterMACD
from plotter.PlotterATR import PlotterATR

from utilities.Constants import Constants


class Plotter:

    legend_id = 0
    def get_legend_position(self):
        legend = [
            "upper left",
            "upper center",
            "upper right",
            "center left",
            "lower left",
            "lower center",
            "lower right",
            "center right", "center", "right", "left"]

        legend_name = legend[Plotter.legend_id % len(legend)]
        Plotter.legend_id += 1
        return legend_name

    current_color_indicator = 0

    def get_next_indicator_color(self):
        av_colors = ["tab:green",
                     "tab:blue",
                     "tab:purple"]

        sel_color = av_colors[Plotter.current_color_indicator % len(av_colors)]
        Plotter.current_color_indicator += 1

        return sel_color

    def __init__(self,
                 period=100
                 ):

        self.fig = {}
        self.ax_main = None
        self.ax_indicators = None
        #self.main_ax_indicator = None

        register_matplotlib_converters()

        self.period = period

        self.volume_color = None
        self.volume_alpha = None
        self.stock_color = None
        self.set_colors()

        self.collapse_indicators = True
        self.axes = None

        Plotter.current_color_indicator = 0
        Plotter.legend_id = 0



    def set_plot_settings(self):
        pass

    def set_colors(self,
                   stock_color="black",
                   volume_color="tab:blue",
                   volume_alpha=0.5):

        self.stock_color = stock_color
        self.volume_color = volume_color
        self.volume_alpha = volume_alpha

    def plot_stock(self, stock, tickers=None, collapse_indicators=True):

        self.legend_id = 0

        if stock is None:
            print("There is no ticker Information, nothing to be plot")
            return

        if tickers is None:
            tickers = stock.ticker

        elif isinstance(tickers, list) is True:
            tickers = tickers

        else:
            tickers = [tickers]

        # TODO: Check what happens here in the iteration
        if self.fig is None or self.ax_main is None or self.ax_indicators is None:

            adj_close_key = Constants.get_adj_close_key()
            volume_key = Constants.get_volume_key()

            price_series = {}
            time_series_volume = {}

            x_series = {}

            for ticker in tickers:
                if (adj_close_key in stock.price_info[ticker]) == False:
                    adj_close_key = Constants.get_close_key()

                x_series[ticker] = stock.price_info[ticker].iloc[-self.period:, :].index

                price_series[ticker] = stock.price_info[ticker].iloc[-self.period:, :][adj_close_key]
                time_series_volume[ticker] = stock.price_info[ticker].iloc[-self.period:, :][volume_key]

                self.ax_main = dict()
                self.ax_indicators = dict()

                if len(stock.indicators) >= 0: #TODO: Remove this

                    subplots = 0
                    if len(stock.indicators) > 0 and collapse_indicators is True:
                        subplots = 2

                    else:
                        subplots = len(stock.indicators)

                    heights_list = [1 for i in range(subplots-1)]
                    heights_list.append(2)

                    fig = plt.figure()
                    self.axes = \
                        fig.subplots(
                            len(stock.indicators),
                            1,
                            sharex='col',
                            gridspec_kw={'height_ratios': heights_list}
                        )





                #     # Plot Line1 (Left Y Axis)
                #     self.fig[ticker], (
                #         self.ax_main[Constants.volume], self.ax_indicators) = \
                #         plt.subplots(
                #             subplots,
                #             1,
                #             figsize=(16, 9),
                #             dpi=80,
                #             sharex=True,
                #             gridspec_kw={'height_ratios': [2, 1]}
                #         )
                # else:
                #
                #     # Plot Line1 (Left Y Axis)
                #     self.fig[ticker], (self.ax_main[Constants.volume]) = \
                #         plt.subplots(
                #             1,
                #             1,
                #             dpi=80,
                #             sharex=True)

                self.set_volume(
                    x_series=x_series[ticker],
                    time_series_volume=time_series_volume[ticker],
                    axis=self.axes[0]
                )

                self.set_stock_price(
                    x_series=x_series[ticker],
                    price_series=price_series[ticker],
                    ticker=ticker,
                    color=self.stock_color)

                for indicator in stock.indicators:
                    self.set_plot_indicator(indicator=indicator,
                                            ticker=ticker,
                                            period=self.period)

        print("plot")

    def set_volume(self, x_series, time_series_volume, axis):

        self.legend_id = 0

        axis.set_ylim(0, time_series_volume.max() * 2)
        axis.tick_params(axis='y', rotation=0, labelcolor=self.volume_color)

        axis.spines["top"].set_alpha(0.0)
        axis.spines["bottom"].set_alpha(1)
        axis.spines["right"].set_alpha(0.0)
        axis.spines["left"].set_alpha(1)

        handles = self.ax_main[Constants.volume].bar(
            x_series,
            time_series_volume,
            color=self.volume_color,
            alpha=self.volume_alpha,
            label='Volume'
        )

        position = self.get_legend_position()
        axis.legend(loc=position)
        axis.set_xlim(
            time_series_volume.iloc[[0]].index,
            time_series_volume.iloc[[-1]].index
        )

    def set_stock_price(self, x_series, price_series, ticker="", color="black"):

        title = "{}".format(ticker)

        # Decorations
        # ax1 (left Y axis)
        # instantiate a second axes that shares the same x-axis
        # TODO: Distinguish between close and adj_close
        self.ax_main[Constants.adj_close] = self.ax_main[Constants.volume].twinx()

        self.ax_main[Constants.adj_close].set_title(title, fontsize=22)
        self.ax_main[Constants.adj_close].tick_params(axis='x', rotation=0, labelsize=12, labelleft=True)
        self.ax_main[Constants.adj_close].set_ylabel('Price', color='black', fontsize=20)
        self.ax_main[Constants.adj_close].tick_params(axis='y', rotation=0, labelcolor=color)
        self.ax_main[Constants.adj_close].grid(alpha=.4)

        self.ax_main[Constants.adj_close].spines["top"].set_alpha(0.0)
        self.ax_main[Constants.adj_close].spines["bottom"].set_alpha(1)
        self.ax_main[Constants.adj_close].spines["right"].set_alpha(0.0)
        self.ax_main[Constants.adj_close].spines["left"].set_alpha(1)

        handles = self.ax_main[Constants.adj_close].plot(x_series, price_series, color=color, label=ticker)
        position = self.get_legend_position()
        self.ax_main[Constants.adj_close].legend(loc=position)

        self.ax_main[Constants.adj_close].set_xlim(
            price_series.iloc[[0]].index,
            price_series.iloc[[-1]].index
        )

    # this has to be called after calling plot_main
    def set_plot_indicator(self, indicator, ticker, color=None, period=100):

        if color is None:
            color = self.get_next_indicator_color()

        plot_indicator = None
        if isinstance(indicator, MACD):
            plot_indicator = PlotterMACD(
                self,
                indicator=indicator,
                ticker=ticker,
                color=color
            )
        if isinstance(indicator, ATR):
            plot_indicator = PlotterATR(
                self,
                indicator=indicator,
                ticker=ticker,
                color=color

            )

        if plot_indicator is not None:
            plot_indicator.plot()
        else:
            print("Plotter for indicator has not been defined.")
            raise ValueError

        self.fig[ticker].tight_layout()

    # this has to be called after calling plot_main
    def plot_indicator(self, df, color="tab:green"):

        self.legend_id = 0

        if self.fig is None or self.ax_indicators is None:
            print("Please call first method plot_main")
            return

        #  Set the layout of the indicators plot
        #  Indicator plot layout
        self.main_ax_indicator.tick_params(axis='y', labelcolor=color, size=20)
        self.main_ax_indicator.grid(alpha=.4)
        self.main_ax_indicator.spines["top"].set_alpha(0.0)
        self.main_ax_indicator.spines["bottom"].set_alpha(1)
        self.main_ax_indicator.spines["right"].set_alpha(0.0)
        self.main_ax_indicator.spines["left"].set_alpha(1)

        indicator_key = df.columns[0]

        time_series_indicator = df.iloc[-self.period:, :][indicator_key]

        self.main_ax_indicator.plot(
            time_series_indicator.index,
            time_series_indicator,
            color=color, label=indicator_key
        )

        position = self.get_legend_position()
        self.main_ax_indicator.legend(loc=position)

        self.main_ax_indicator.set_xlim(
            time_series_indicator.iloc[[0]].index,
            time_series_indicator.iloc[[-1]].index
        )
