from plotter.PlotterIndicator import PlotterIndicator


class PlotterMACD(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, period, color="tab:green"):
        super().__init__(plotter, indicator, ticker, period, color)
        self.signal_color = "tab:orange"


    def plot(self, axis):

        print("Plotting MACD")

        self.plot_indicator(
            axis=axis
        )

        self.plot_indicator(
            axis=axis,
            series=self.indicator.df[self.ticker][[self.indicator.signal_key]],
            label=self.indicator.signal_key,
            color=self.signal_color
        )

        legend_position = self.plotter.get_legend_position()
        axis.legend(loc=legend_position)

        return self.plotter





