import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from plotter.PlotterIndicator import PlotterIndicator


from utilities.Constants import Constants


class PlotterATR(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, color="tab:green"):
        super().__init__(plotter, indicator, ticker, color)


    def plot(self, axis):
        super().plot(axis)
        return self.plotter







