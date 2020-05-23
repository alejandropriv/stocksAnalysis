import abc
from utilities.Constants import Constants



class Indicator(metaclass=abc.ABCMeta):


        @abc.abstractmethod
        def __init__(self):
            self.ticker = None
            self.df = None

        @abc.abstractmethod
        def set_input_data(self, df):
            if df is None:
                print("Error: data not found")
                raise IOError

            self.ticker = df.ticker


        @abc.abstractmethod
        def calculate(self):
            """function to calculate the indicator"""
            if self.df is None:
                print("Error: data not found")
                raise IOError


        @abc.abstractmethod
        def plot(self, plotter=None, period=100, color="tab:green"):
            self.plot(plotter, period, key, color, None)


        def plot_indicator(self, plotter=None, period=100, key=None, color="tab:green", legend_position=None):

            if legend_position is None:
                legend_position = plotter.get_legend_position()

            print("Plotting {}".format(key))

            max_value = self.df[key].max()
            min_value = self.df[key].min()

            if plotter.ax_indicators is None or len(plotter.ax_indicators) <= 1:
                print("This is the first indicator, in the plot")
                plotter.ax_indicators[key] = plotter.ax_indicators[Constants.main_indicator_axis]

            else:
                print("This indicator is added to the current plot")
                # instantiate a second axes that shares the same x-axis
                plotter.ax_indicators[key] = plotter.ax_indicators[Constants.main_indicator_axis].twinx()

            plotter.ax_indicators[key].set_ylim(min_value - 1, max_value + 1)

            plotter.ax_indicators[key].legend(loc=legend_position)

            plotter.main_ax_indicator = plotter.ax_indicators[key]

            plotter.plot_indicator(df=self.df[[key]], period=period, color=color)

