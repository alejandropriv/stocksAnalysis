from fundamentals.Fundamentals import Fundamentals
from data.YahooAPIHistoricalData import YahooAPIHistoricalData
from data.YahooFinancialsHistoricalData import YahooFinancialsHistoricalData
from data_analysis.DailyReturn import DailyReturn


class Stock:

    error = None

    fundamentals = None

    tickers = None

    data_source = None

    time_series = None

    daily_return = None


    # Put here an enum and a case with the enum
    def __init__(self, tickers=None, data_source=None):

        if tickers is None:
            raise ValueError

        if data_source is None:
            data_source = YahooAPIHistoricalData()

        print("Stock {} created".format(tickers))
        self.tickers = tickers
        self.data_source = data_source



    def set_data_source(self, data_source_type):
        if data_source_type == YahooAPIHistoricalData.DATASOURCETYPE.YAHOOFINANCIALS:
            self.data_source = YahooFinancialsHistoricalData()

        if data_source_type == YahooAPIHistoricalData.DATASOURCETYPE.YAHOOAPI:
            self.data_source = YahooAPIHistoricalData()


    def get_fundamentals(self):
        self.fundamentals = {}
        for ticker in self.tickers:
            self.fundamentals[ticker] = Fundamentals(ticker)
            self.fundamentals[ticker].get_data()


    def get_historical_data(self):
        self.data_source.extract_historical_data(self.tickers)


    def get_statistical_data(self, period):

        if self.data_source.adj_close is None:
            print("Unable to get statistical data because there is no data, calling 'self.get_historical_data()' first")
            self.get_historical_data()


        self.daily_return = DailyReturn(self.get_prices_close_adj(), period)
        self.daily_return.get_statistical_data()



    def get_prices_close_adj(self):

        method_tag = "get_prices_close_adj"

        if self.data_source is not None:
            if self.data_source.adj_close is not None:
                prices = self.data_source.adj_close

            else:
                print("Getting Historical data first")
                self.get_historical_data()
                prices = self.data_source.adj_close

        else:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        if prices.empty == True:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        return prices


    def get_volume(self):

        method_tag = "get_volume"

        if self.data_source is not None:
            if self.data_source.volume is not None:
                volume = self.data_source.volume

            else:
                print("Getting Historical data first")
                self.get_historical_data()
                volume = self.data_source.volume

        else:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        if volume.empty == True:
            print("There has been an error in {}".format(method_tag))
            raise ValueError


        return volume
