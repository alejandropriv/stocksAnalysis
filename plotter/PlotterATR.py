import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from plotter.PlotterIndicator import PlotterIndicator


from utilities.Constants import Constants


class PlotterATR(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, color="tab:green"):
        super().__init__(plotter, indicator, ticker, color)


    def plot(self):

        print("Plotting ATR")

        max_value = self.indicator.df[self.ticker][self.indicator.indicator_key].max()
        min_value = self.indicator.df[self.ticker][self.indicator.indicator_key].min()

        if self.plotter.ax_indicators is None or len(self.plotter.ax_indicators) <= 1:
            self.plotter.ax_indicators[self.indicator.indicator_key] = self.plotter.ax_indicators[Constants.main_indicator_axis]

        else:
            # instantiate a second axes that shares the same x-axis
            self.plotter.ax_indicators[self.indicator.indicator_key] = \
                self.plotter.ax_indicators[Constants.main_indicator_axis].twinx()

        self.plotter.ax_indicators[self.indicator.indicator_key].set_ylim(min_value - 1, max_value + 1)

        self.plotter.main_ax_indicator = self.plotter.ax_indicators[self.indicator.indicator_key]
        self.plotter.main_ax_indicator.tick_params(axis='y', labelcolor=self.tick_y_color, size=20)

        self.plotter.plot_indicator(
                df=self.indicator.df[self.ticker][[self.indicator.indicator_key]],
                color=self.main_color
        )

        legend_position = self.plotter.get_legend_position()
        self.plotter.ax_indicators[self.indicator.indicator_key].legend(loc=legend_position)

        return self.plotter





