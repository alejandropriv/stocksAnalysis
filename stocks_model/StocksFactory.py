from data.DataSource import DataSource


from data.PandasDataReaderDataSource import PandasDataReaderDataSource
from data.YFinanceDataSource import YFinanceDataSource
from utilities.Constants import Constants
from stocks_model.Stock import Stock

import datetime


class StocksFactory:

    # Put here an enum and a case with the enum
    def __init__(self,
                 data_source=None,
                 bulk=False):


        self.create_stocks(
            data_source,
            bulk
        )



    def create_stocks(self, data_source=None, bulk=False):
        if data_source is None:
            print("Error: Define your data source first !!!.")
            return

        if data_source.tickers is None:
            print("Error: Set Historical data")
            return

        if bulk is True:
            print("This option has not been already programmed! wait for next release")


        else:
            for ticker in self.tickers:
                stock = Stock(tickers=ticker, data_source=self.data_source)

                self.stocks.append(stock)



