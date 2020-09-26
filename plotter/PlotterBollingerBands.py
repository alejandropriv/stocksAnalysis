import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from plotter.PlotterIndicator import PlotterIndicator


from utilities.Constants import Constants


class PlotterBollingerBands(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, color="tab:green"):
        super().__init__(plotter, indicator, ticker, color)



    def plot(self, axis):
        super().plot(plotter=plotter, period=period, color=color)

        x = self.df.iloc[:, [0]]
        index = x.iloc[-period:, :].index

        # put period for the data also
        df = self.df.iloc[-period:, :]

        if plotter.ax_main is None:
            print("Error: Main Stock has not been plotted, "
                  "plot a stock and then plot the associated bollinger bands")
            raise IOError

        plotter.ax_main[Constants.adj_close].plot(index, df[self.bb_down_key], color=color)
        plotter.ax_main[Constants.adj_close].plot(index, df[self.bb_up_key], color=color)





