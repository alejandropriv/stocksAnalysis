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
                 data_source_type=DataSource.DATASOURCETYPE.YFINANCE,
                 bulk=True,
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




        self.bulk = bulk
        self.group = group

        self.stocks = []
        self.create_stocks()

        self.end_date = None
        self.time_series = None
        self.start_date = None



    def set_data_source(self, data_source_type):
        if data_source_type is DataSource.DATASOURCETYPE.PANDASDATAREADER:
            self.data_source = PandasDataReaderDataSource()

        elif data_source_type is DataSource.DATASOURCETYPE.YFINANCE:
            self.data_source = YFinanceDataSource()

        elif data_source_type is DataSource.DATASOURCETYPE.ALPHA:
            self.data_source = None  #TODO

        elif data_source_type is DataSource.DATASOURCETYPE.YAHOOFINANCIALS:
            self.data_source = None  #TODO



    def get_fundamentals(self):
        for stock in self.stocks:
            stock.get_fundamentals()

    def get_historical_data(self,
                            end_date=datetime.datetime.now(),
                            start_date=None,
                            time_delta=None,
                            time_series=Constants.INTERVAL.DAY,
                            ):

        self.time_series = time_series

        if end_date is None:
            print("Error: end_date is None, verify function call ")
            return
        else:
            self.end_date = end_date

        if start_date is not None:
            if start_date < end_date:
                self.start_date = start_date
            else:
                print("Error:  Start_date should be earlier than end date")
                return


        elif time_delta is not None:
            self.start_date = datetime.datetime.today() - datetime.timedelta(time_delta)


        else:
            print("Error: Neither the Start_date nor the time_delta were defined ")
            return

        for stock in self.stocks:
            stock.get_historical_data(start_date=self.start_date,
                                      end_date=self.end_date,
                                      interval=self.time_series)



    def create_stocks(self):
        if self.tickers is None:
            print("Error: Define your tickers first !!!.")
            return

        if self.bulk is False:
            print("This option has not been already programmed! wait for next release")


        else:
            for ticker in self.tickers:
                stock = Stock(tickers=ticker, data_source=self.data_source)

                self.stocks.append(stock)



