import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from plotter.PlotterIndicator import PlotterIndicator


from utilities.Constants import Constants


class PlotterMACD(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, color="tab:green"):
        super().__init__(plotter, indicator, ticker, color)
        self.signal_color = "tab:orange"
        self.tick_y_color = "tab:green"


    def plot(self):

        print("Plotting MACD")

        max_value = self.indicator.df[self.ticker][self.indicator.macd_key].max()
        min_value = self.indicator.df[self.ticker][self.indicator.macd_key].min()

        if self.plotter.ax_indicators is None or len(self.plotter.ax_indicators) <= 1:
            self.plotter.ax_indicators[self.indicator.macd_key] = self.plotter.ax_indicators[Constants.main_indicator_axis]

        else:
            # instantiate a second axes that shares the same x-axis
            self.plotter.ax_indicators[self.indicator.macd_key] = \
                self.plotter.ax_indicators[Constants.main_indicator_axis].twinx()

        self.plotter.ax_indicators[self.indicator.macd_key].set_ylim(min_value - 1, max_value + 1)

        self.plotter.main_ax_indicator = self.plotter.ax_indicators[self.indicator.macd_key]
        self.plotter.main_ax_indicator.tick_params(axis='y', labelcolor=self.tick_y_color, size=20)

        self.plotter.plot_indicator(
                df=self.indicator.df[self.ticker][[self.indicator.macd_key]],
                color=self.main_color
        )
        self.plotter.plot_indicator(
                df=self.indicator.df[self.ticker][[self.indicator.signal_key]],
                color=self.signal_color
        )

        legend_position = self.plotter.get_legend_position()
        self.plotter.ax_indicators[self.indicator.macd_key].legend(loc=legend_position)

        return self.plotter





