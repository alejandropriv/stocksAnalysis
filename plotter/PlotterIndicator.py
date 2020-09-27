import abc

class PlotterIndicator(metaclass=abc.ABCMeta):


    def __init__(self, plotter, indicator, ticker, color="tab:green"):

        self.indicator = indicator
        self.ticker = ticker

        if plotter is None:
            print("Error: plotter Object not found, please Select the main stock first.")
            raise IOError

        self.plotter = plotter
        self.main_color = color
        self.tick_y_color = color




    def plot(self, axis):


        print("Plotting Indicator")


        limit_y = self.calculate_limit_y()
        axis.set_ylim(limit_y[0], limit_y[1])

        axis.tick_params(axis='y', labelcolor=self.tick_y_color, size=20)

        self.plotter.plot_indicator(
            df=self.indicator.df[self.ticker][[self.indicator.indicator_key]],
            axis=axis,
            color=self.main_color
        )

        legend_position = self.plotter.get_legend_position()
        axis.legend(loc=legend_position)

        return self.plotter


    def calculate_limit_y(self):

        max_value = self.indicator.df[self.ticker][self.indicator.indicator_key].max()
        min_value = self.indicator.df[self.ticker][self.indicator.indicator_key].min()

        return [min_value, max_value]


