import abc



class PlotterIndicator:


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


        main_key = None
        available_indicators = ["MACD", "ATR"]

        for key in self.indicator.df[self.ticker].columns:
            if key in available_indicators:
                main_key = key
                break


        self.plotter.plot_indicator(
            df=self.indicator.df[self.ticker][[main_key]],
            axis=axis,
            color=self.main_color
        )





