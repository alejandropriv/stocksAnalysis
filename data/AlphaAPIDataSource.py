from data.DataSource import DataSource
import datetime


class AlphaAPIDataSource(HistoricalData):


    def __init__(self,
                 ticker,
                 start_date=(datetime.date.today() - datetime.timedelta(1825)).strftime('%Y-%m-%d'),
                 end_date=(datetime.date.today()).strftime('%Y-%m-%d'),
                 time_series=HistoricalData.TIMESERIES.DAILY,
                 data_columns=None):

        if data_columns is None:
            data_columns = ["all"]

        super().__init__(ticker,
                         start_date,
                         end_date,
                         time_series,
                         data_columns
                         )




        # PlotData.set_interactive_mode(True)
        #
        # i = len(self.tickers)
        #
        # for symbol_str in self.tickers:
        #
        #     i -= 1
        #     if i == 0:
        #         PlotData.set_interactive_mode(False)
        #
        #     stock_plot = StockPlot(self.apikey, symbol_str)
        #     stock_plot.retrieve_daily_data(True)
        #     stock_plot.print_metadata()
        #     stocks = []
        #
        #     stocks.append(stock_plot)