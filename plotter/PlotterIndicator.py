import abc

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters


from utilities.Constants import Constants


class PlotterIndicator:


    def __init__(self, plotter, indicator, ticker, period=100, color="tab:green"):

        self.indicator = indicator
        self.ticker = ticker

        if plotter is None:
            print("Error: plotter Object not found, please Select the main stock first.")
            raise IOError

        self.plotter = plotter
        self.period = period
        self.color = color


    @abc.abstractmethod
    def plot(self):
        pass





