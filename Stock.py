from fundamentals.Fundamentals import Fundamentals
from Data.YahooAPIDataSource import YahooAPIDataSource
from Data.YahooFinancialsDataSource import YahooFinancialsDataSource




class Stock:

    error = None

    fundamentals = None

    ticker = None

    data_source = None



    def __init__(self, ticker):
        print("Stock {} created".format(ticker))
        self.ticker = ticker
        self.data_source = YahooAPIDataSource(ticker)


    def __init_(self, ticker, data_source): # Put here an enum and a case with the enum
        print("Stock {} created".format(ticker))
        self.ticker = ticker
        self.data_source = data_source

    def set_data_source(self, data_source_type):
        if data_source_type == YahooAPIDataSource.DataSourceType.YAHOOFINANCIALS:
            self.data_source = YahooFinancialsDataSource(ticker=self.ticker)


    def get_fundamentals(self):
        self.fundamentals = Fundamentals(self.ticker)
        self.fundamentals.get_data()


    def get_historical_data(self):
        self.data_source.extract_historical_data()







