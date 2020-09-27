import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from plotter.PlotterIndicator import PlotterIndicator


from utilities.Constants import Constants


class PlotterRSI(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, color="tab:green"):
        super().__init__(plotter, indicator, ticker, color)



    def plot(self, axis):
        super().plot(axis)
        return self.plotter


    def calculate_limit_y(self):

        max_value = 100
        min_value = 0

        return [min_value, max_value]



