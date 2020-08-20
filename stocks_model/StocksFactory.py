from data.DataSource import DataSource


from data.PandasDataReaderDataSource import PandasDataReaderDataSource
from data.YFinanceDataSource import YFinanceDataSource
from utilities.Constants import Constants
from stocks_model.Stock import Stock

import datetime


class StocksFactory:

    # Put here an enum and a case with the enum
    def __init__(self):
        pass



    @staticmethod
    def create_stocks(data_source=None, bulk=False):

        stocks = []
        if data_source is None:
            print("Error: Define your data source first !!!.")
            return

        if data_source.tickers is None:
            print("Error: Set Historical data")
            return

        if bulk is True: #print("This option has not been already programmed! wait for next release")

            stock = Stock(tickers=data_source.tickers, data_source=data_source)
            stocks.append(stock)

        else:
            for ticker in data_source.tickers:
                stock = Stock(tickers=[ticker], data_source=data_source)

                stocks.append(stock)


        return stocks
