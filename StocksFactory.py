from data.DataSource import DataSource


from data.PandasDataReaderDataSource import PandasDataReaderDataSource
from data.YFinanceDataSource import YFinanceDataSource
from utilities.Constants import Constants
from Stock import Stock

import datetime


class StocksFactory:

    # Put here an enum and a case with the enum
    def __init__(self,
                 tickers=None,
                 end_date=datetime.datetime.now(),
                 start_date=None,
                 time_delta= None,
                 time_series=Constants.INTERVAL.DAY,
                 data_source_type=DataSource.DATASOURCETYPE.YFINANCE,
                 bulk=False,
                 group=1):

        self.bulk = bulk
        self.group = group

        if tickers is None:
            print("Error: Define your tickers first !!!.")
            return

        self.tickers = tickers
        print("Tickers for: {} created".format(self.tickers))

        self.data_source = None
        self.set_data_source(data_source_type)

        self.time_series = time_series

        self.end_date = end_date

        self.start_date = None


        if start_date is not None:
            self.start_date = start_date

        elif time_delta is not None:
            self.start_date = datetime.date.today() - datetime.timedelta(time_delta)

        else:
            print("Error: Neither the Start_date nor the time_delta were defined ")
            return
            #TODO: Put here a default interval per timeSeries



        self.stocks = []

        self.bulk = bulk
        self.group = group


    def set_data_source(self, data_source_type):
        if data_source_type is DataSource.DATASOURCETYPE.PANDASDATAREADER:
            self.data_source = PandasDataReaderDataSource()

        elif data_source_type is DataSource.DATASOURCETYPE.YFINANCE:
            self.data_source = YFinanceDataSource()

        elif data_source_type is DataSource.DATASOURCETYPE.ALPHA:
            self.data_source = None  #TODO

        elif data_source_type is DataSource.DATASOURCETYPE.YAHOOFINANCIALS:
            self.data_source = None  #TODO


    def createStocks(self):
        if self.tickers is None:
            print("Error: Define your tickers first !!!.")
            return

        if self.start_date is None:
            print("Error: Define a startDate or a timeDelta.")
            return

        if self.bulk is False:
            print("This option has not been already programmed! wait for next release")


        else:
            for ticker in self.tickers:
                stock = Stock(tickers=ticker, data_source=self.data_source)
                stock.get_historical_data(start_date=self.start_date,
                                          end_date=self.end_date,
                                          interval=self.time_series)

                self.stocks.append(stock)



