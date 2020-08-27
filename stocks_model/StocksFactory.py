
from utilities.Constants import Constants
from stocks_model.Stock import Stock

from data.DataCollector import DataCollector

import datetime


class StocksFactory:

    def __init__(self):
        pass

    @staticmethod
    def create_stocks(
            tickers,
            data_source_type,
            start_date=datetime.date.today() - datetime.timedelta(1),
            end_date=datetime.date.today(),
            period=None,
            interval=Constants.INTERVAL.DAY,
            fundamentals=True,
            historical=True,
            indicators=None,
            bulk=False
    ):


        stocks = None

        data_collector = \
            DataCollector(
                tickers=tickers,
                data_source_type=data_source_type,
                fundamentals=fundamentals,
                historical=historical,
                start_date=start_date,
                end_date=end_date,
                period=period,
                interval=interval
            )
        if historical is True:
            data_source = \
                data_collector.extract_historical_data()

            stocks = StocksFactory.load_stocks(data_source, bulk)
            stocks = StocksFactory.load_indicators(stocks, indicators)

        if fundamentals is True:
            pass



        return stocks

    @staticmethod
    def load_stocks(data_source=None, bulk=False, indicators=None):

        stocks = []
        if data_source is None:
            print("Error: Define your data source first !!!.")
            return

        if data_source.tickers is None:
            print("Error: Set Historical data")
            return

        if bulk is True:  # print("This option has not been already programmed! wait for next release")

            stock = Stock(ticker=data_source.tickers, data_source=data_source)
            stocks.append(stock)

        else:
            for ticker in data_source.tickers:
                stock = Stock(ticker=ticker, data_source=data_source)
                stock = StocksFactory.load_indicators(stock, indicators)

                stocks.append(stock)

        return stocks



    @staticmethod
    def load_indicators(stock, indicators):

        if indicators is None:
            indicators = []

        for indicator in indicators:
            stock.append_indicator(indicator)

        return stock
