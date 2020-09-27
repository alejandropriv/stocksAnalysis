import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from indicators.MACD import MACD
from indicators.ATR import ATR
from indicators.RSI import RSI
from indicators.BollingerBands import BollingerBands


from plotter.PlotterMACD import PlotterMACD
from plotter.PlotterATR import PlotterATR
from plotter.PlotterRSI import PlotterRSI
from plotter.PlotterBollingerBands import PlotterBollingerBands


from utilities.Constants import Constants


class Plotter:

    legend_id = 0
    @staticmethod
    def get_legend_position():
        legend = [
            "upper left",
            "upper center",
            "upper right",
            "center left",
            "lower left",
            "lower center",
            "lower right",
            "center right", "center", "right"]

        legend_name = legend[Plotter.legend_id % len(legend)]
        Plotter.legend_id += 1
        return legend_name


    current_color_indicator = 0

    @staticmethod
    def get_next_indicator_color():
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
        self.axes_main = None
        self.axes_indicators = None

        register_matplotlib_converters()

        self.period = period

        self.collapse_indicators = True

        self.x_series = None
        self.volume_series = None
        self.price_series = None

        self.volume_color = None
        self.volume_alpha = None
        self.stock_color = None
        self.set_colors()

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

        Plotter.legend_id = 0

        if stock is None:
            print("There is no ticker Information, nothing to be plot")
            return

        if tickers is None:
            tickers = stock.ticker

        elif isinstance(tickers, list) is True:
            tickers = tickers

        else:
            tickers = [tickers]


        if self.fig is None or self.axes_main is None or self.axes_indicators is None:

            adj_close_key = Constants.get_adj_close_key()
            volume_key = Constants.get_volume_key()

            self.price_series = {}
            self.volume_series = {}

            self.x_series = {}

            for ticker in tickers:
                if (adj_close_key in stock.price_info[ticker]) == False:
                    adj_close_key = Constants.get_close_key()

                self.x_series[ticker] = stock.price_info[ticker].iloc[-self.period:, :].index

                self.price_series[ticker] = stock.price_info[ticker].iloc[-self.period:, :][adj_close_key]
                self.volume_series[ticker] = stock.price_info[ticker].iloc[-self.period:, :][volume_key]

                self.axes_main = dict()
                self.axes_indicators = dict()


                if len(stock.indicators) > 0 and collapse_indicators is True:
                    subplots = 2

                else:
                    subplots = len(stock.indicators)+1

                heights_list = [1 for i in range(subplots-1)]
                heights_list.insert(0, 2)

                self.fig = plt.figure(figsize=(8, 6), dpi=80)
                axes = \
                    self.fig.subplots(
                        subplots,
                        1,
                        sharex='col',
                        gridspec_kw={'height_ratios': heights_list}
                    )

                self.axes_main[Constants.volume_axis] = axes[0]
                self.axes_indicators = axes[1:]


                self.set_volume(
                    ticker=ticker
                )

                self.set_stock_price(
                    ticker=ticker,
                    color=self.stock_color
                )

                i = 0
                indicator_axis = self.axes_indicators[i]

                for indicator in stock.indicators:
                    if collapse_indicators == True :

                        if i > 0:
                            indicator_axis = indicator_axis.twinx()

                        i += 1

                    else:
                        indicator_axis = self.axes_indicators[i]
                        i += 1


                    self.set_plot_indicator(indicator=indicator,
                                            ticker=ticker,
                                            axis=indicator_axis)

        print("plot")

    def set_volume(self, ticker):

        Plotter.legend_id = 0

        self.axes_main[Constants.volume_axis].set_ylim(0, self.volume_series[ticker].max() * 2)
        self.axes_main[Constants.volume_axis].tick_params(axis='y', rotation=0, labelcolor=self.volume_color)

        self.axes_main[Constants.volume_axis].spines["top"].set_alpha(0.0)
        self.axes_main[Constants.volume_axis].spines["bottom"].set_alpha(1)
        self.axes_main[Constants.volume_axis].spines["right"].set_alpha(0.0)
        self.axes_main[Constants.volume_axis].spines["left"].set_alpha(1)

        # Constants.volume
        handles = self.axes_main[Constants.volume_axis].bar(
            self.x_series[ticker],
            self.volume_series[ticker],
            color=self.volume_color,
            alpha=self.volume_alpha,
            label='Volume'
        )

        position = self.get_legend_position()
        self.axes_main[Constants.volume_axis].legend(loc=position)
        self.axes_main[Constants.volume_axis].set_xlim(
            self.volume_series[ticker].iloc[[0]].index,
            self.volume_series[ticker].iloc[[-1]].index
        )

    def set_stock_price(self, ticker="", color="black"):

        title = "{}".format(ticker)


        # ax1 (left Y axis)
        # instantiate a second axes that shares the same x-axis
        # twin volume axis
        self.axes_main[Constants.prices_axis] = self.axes_main[Constants.volume_axis].twinx()

        self.axes_main[Constants.prices_axis].set_title(title, fontsize=22)
        self.axes_main[Constants.prices_axis].tick_params(axis='x', rotation=0, labelsize=12, labelleft=True)
        self.axes_main[Constants.prices_axis].set_ylabel('Price', color='black', fontsize=20)
        self.axes_main[Constants.prices_axis].tick_params(axis='y', rotation=0, labelcolor=color)
        self.axes_main[Constants.prices_axis].grid(alpha=.4)

        self.axes_main[Constants.prices_axis].spines["top"].set_alpha(0.0)
        self.axes_main[Constants.prices_axis].spines["bottom"].set_alpha(1)
        self.axes_main[Constants.prices_axis].spines["right"].set_alpha(0.0)
        self.axes_main[Constants.prices_axis].spines["left"].set_alpha(1)

        handles = self.axes_main[Constants.prices_axis].plot(self.x_series[ticker], self.price_series[ticker], color=color, label=ticker)
        position = Plotter.get_legend_position()
        self.axes_main[Constants.prices_axis].legend(loc=position)


        self.axes_main[Constants.prices_axis].set_xlim(
            self.price_series[ticker].iloc[[0]].index,
            self.price_series[ticker].iloc[[-1]].index
        )

    # this has to be called after calling plot_main
    def set_plot_indicator(self, indicator, ticker, axis, color=None):

        if color is None:
            color = self.get_next_indicator_color()

        plot_indicator = None
        if isinstance(indicator, MACD):
            plot_indicator = PlotterMACD(
                self,
                indicator=indicator,
                ticker=ticker,
                period=self.period,
                color=color
            )
        if isinstance(indicator, ATR):
            plot_indicator = PlotterATR(
                self,
                indicator=indicator,
                ticker=ticker,
                period=self.period,
                color=color

            )
        if isinstance(indicator, RSI):
            plot_indicator = PlotterRSI(
                self,
                indicator=indicator,
                ticker=ticker,
                period=self.period,
                color=color

            )

        if isinstance(indicator, BollingerBands):
            plot_indicator = PlotterBollingerBands(
                self,
                indicator=indicator,
                ticker=ticker,
                period=self.period,
                color=color

            )

        if plot_indicator is not None or self.fig is None or axis is None:
            plot_indicator.plot(axis)

        else:
            print("Plotter for indicator has not been defined, Verify plot configuration")
            raise ValueError
