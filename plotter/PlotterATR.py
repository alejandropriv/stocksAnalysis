import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from plotter.PlotterIndicator import PlotterIndicator


from utilities.Constants import Constants


class PlotterATR(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, color="tab:green"):
        super().__init__(plotter, indicator, ticker, color)


    def plot(self, axis):

        print("Plotting ATR")

        max_value = self.indicator.df[self.ticker][self.indicator.indicator_key].max()
        min_value = self.indicator.df[self.ticker][self.indicator.indicator_key].min()


        axis.set_ylim(min_value - 1, max_value + 1)

        axis.tick_params(axis='y', labelcolor=self.tick_y_color, size=20)

        self.plotter.plot_indicator(
            df=self.indicator.df[self.ticker][[self.indicator.indicator_key]],
            axis=axis,
            color=self.main_color
        )

        legend_position = self.plotter.get_legend_position()
        axis.legend(loc=legend_position)

        return self.plotter





