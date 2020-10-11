from utilities.Constants import Constants
from stocks_model.Stock import Stock

from data.DataCollector import DataCollector

import datetime
import pandas as pd
import copy


class StocksFactory:

    def __init__(self):
        pass

    # Fix this was created to fix the problem of having only one stock (input dataframe is different)
    # This should be removed and dataframe handled accordingly
    @staticmethod
    def add_SPI500_ticker(tickers):
        tickers.append("^GSPC")
        return tickers

    @staticmethod
    def create_stocks(
            strategy,
            tickers,
            bulk=True,

    ):

        tickers = StocksFactory.add_SPI500_ticker(tickers=tickers)


# TODO: Check if still Getting prices is being executed twice
        data_collector = \
            DataCollector(
                tickers=tickers,
                strategy=strategy
            )

        data_source_historical = None
        data_source_fundamentals = None

        if data_collector.data_source_historical is not None:
            data_source_historical = \
                data_collector.extract_historical_data()

        if data_collector.data_source_fundamentals is not None:
            data_source_fundamentals = \
                data_collector.extract_fundamentals()


        indicators = strategy.indicators
        stocks = StocksFactory.load_stocks(data_source_historical=data_source_historical,
                                           data_source_fundamentals=data_source_fundamentals,
                                           bulk=bulk,
                                           indicators=indicators)

        return stocks

    @staticmethod
    def load_stocks(data_source_historical=None, data_source_fundamentals=None, bulk=False, indicators=None):

        stocks = []
        if data_source_historical is None and data_source_fundamentals is None:
            print("Error: Define your data sources first !!!.")
            return

        if data_source_historical is not None:
            tickers = data_source_historical.tickers

        elif data_source_fundamentals is not None:
            tickers = data_source_fundamentals.tickers

        else:
            print("Error: Set Historical data")
            return


        if bulk is True:  # print("This option has not been already programmed! wait for next release")

            stock = Stock(ticker=tickers,
                          data_source_historical=data_source_historical,
                          data_source_fundamentals=data_source_fundamentals)

            stock = StocksFactory.load_indicators(stock, indicators)
            stocks.append(stock)

        else:
            for ticker in tickers:

                data_source_stock = None
                if data_source_historical is not None:
                    data_source_stock = copy.copy(data_source_historical)
                    data_source_stock.prices = pd.DataFrame()

                    data_source_stock.prices = pd.concat([data_source_historical.prices[ticker]], axis=1, keys=[ticker])


                stock = Stock(ticker=[ticker],
                              data_source_historical=data_source_stock,
                              data_source_fundamentals=data_source_fundamentals)

                stock = StocksFactory.load_indicators(stock, indicators)

                stocks.append(stock)

        return stocks

    @staticmethod
    def load_indicators(stock, indicators):

        if indicators is None:
            indicators = []

        for indicator in indicators:
            stock.append_indicator(copy.copy(indicator))

        return stock
