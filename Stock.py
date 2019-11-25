from fundamentals.Fundamentals import Fundamentals
from data.YahooAPIHistoricalData import YahooAPIHistoricalData
from data.YahooFinancialsHistoricalData import YahooFinancialsHistoricalData




class Stock:

    error = None

    fundamentals = None

    tickers = None

    data_source = None

    time_series = None



    # Put here an enum and a case with the enum
    def __init__(self, tickers=None, data_source=None):

        if tickers is None:
            raise ValueError

        if data_source is None:
            data_source = YahooAPIHistoricalData()

        print("Stock {} created".format(tickers))
        self.tickers = tickers
        self.fundamentals = {}
        self.data_source = data_source



    def set_data_source(self, data_source_type):
        if data_source_type == YahooAPIHistoricalData.DATASOURCETYPE.YAHOOFINANCIALS:
            self.data_source = YahooFinancialsHistoricalData()

        if data_source_type == YahooAPIHistoricalData.DATASOURCETYPE.YAHOOAPI:
            self.data_source = YahooAPIHistoricalData()



    def get_fundamentals(self):
        for ticker in self.tickers:
            self.fundamentals[ticker] = Fundamentals(ticker)
            self.fundamentals[ticker].get_data()


    def get_historical_data(self):
        self.data_source.extract_historical_data(self.tickers)
