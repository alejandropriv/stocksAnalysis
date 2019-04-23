from alpha_vantage.timeseries import TimeSeries
from PlotData import PlotData


class Stock:
    apikey = None
    data = None
    meta_data = None
    symbol = None
    data_plot = None
    plot_number = 0;

    def __init__(self, _apikey):
        print("Stock created")

        self.init_parameters(_apikey)

    def __init__(self, _apikey, _symbol):

        self.symbol = _symbol

        print("Stock {0} created".format(self.symbol))

        self.init_parameters(_apikey)

    def init_parameters(self, _apikey):
        self.apikey = _apikey

    def retrieve_daily_data(self, plot=False, _outputsize='compact'):

        ts = TimeSeries(key=self.apikey, output_format='pandas')

        self.data, self.meta_data = ts.get_daily(symbol=self.symbol,
                                                 outputsize=_outputsize)  # , interval='1min', outputsize='full')

        if plot is True:

            self.data_plot = PlotData(self)
            self.data_plot.plot_close()

    def print_metadata(self):
        print(self.meta_data)
