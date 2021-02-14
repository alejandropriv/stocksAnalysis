from plotter.PlotterIndicator import PlotterIndicator

import abc
import plotter.Plotter as Plotter
from utilities.Constants import Constants



class PlotterKPI(metaclass=abc.ABCMeta):

    def __init__(self, plotter, kpi_series, ticker, period, color="tab:green"):

        self.kpi_series = kpi_series
        self.ticker = ticker
        self.axes_main = None


        if plotter is None:
            print("Error: plotter Object not found, please Select the main stock first.")
            raise IOError

        self.plotter = plotter
        self.main_color = color
        self.tick_y_color = color
        self.period = period

    def plot_kpi(self, ticker):

        Plotter.legend_id = 0
        Plotter.current_color_indicator = 0


        self.axes_main[Constants.get_key("CAGR")].set_ylim(0, self.kpi_series[ticker].max() * 1.2)
        self.axes_main[Constants.volume_axis].tick_params(
            axis='y',
            rotation=0,
            labelcolor=self.main_color)

        self.axes_main[Constants.volume_axis].spines["top"].set_alpha(0.0)
        self.axes_main[Constants.volume_axis].spines["bottom"].set_alpha(1)
        self.axes_main[Constants.volume_axis].spines["right"].set_alpha(0.0)
        self.axes_main[Constants.volume_axis].spines["left"].set_alpha(1)

        # Constants.volume

        self.axes_main[Constants.volume_axis].bar(
            self.x_series[ticker],
            self.kpi_series[ticker],
            color=self.main_color,
            alpha=1,
            label='CAGR'
        )

        position = Plotter.get_legend_position()
        self.axes_main[Constants.volume_axis].legend(loc=position)

