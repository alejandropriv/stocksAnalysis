from plotter.PlotterIndicator import PlotterIndicator


class PlotterMACD(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, period, color="tab:green"):
        super().__init__(plotter, indicator, ticker, period, color)
        self.signal_color = "tab:orange"


    def plot(self, axis):

        print("Plotting MACD")



        self.plot_indicator(
            axis=axis,
            df=self.indicator.df[self.ticker][[self.indicator.signal_key]],
            label=self.indicator.signal_key,
            color=self.signal_color
        )

        self.plot_indicator(
            axis=axis
        )

        return self.plotter





