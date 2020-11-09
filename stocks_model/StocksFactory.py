from stocks_model.Stock import Stock

from data.DataCollector import DataCollector

import pandas as pd
import copy


class StocksFactory:


    # TODO: Fix this was created to fix the problem of having only one stock (input dataframe is different)
    # This should be removed and dataframe handled accordingly
    @staticmethod
    def add_spi500_ticker(tickers):
        tickers.append("^GSPC")
        return tickers

    @staticmethod
    def create_stocks(strategy, tickers, bulk=True):

        tickers = StocksFactory.add_spi500_ticker(tickers=tickers)


# TODO: Check if still Getting prices is being executed twice

        data_source_historical = None
        data_source_fundamentals = None

        data_sources = \
            DataCollector.get_data_sources(
                strategy.data_source_type_historical,
                strategy.data_source_type_fundamentals
            )

        if DataCollector.HISTORICAL_KEY in data_sources.keys():
            data_source_historical = data_sources[DataCollector.HISTORICAL_KEY]


            if data_source_historical is not None:
                data_source_historical.extract_historical_data(
                    tickers=tickers,
                    start_date=strategy.start_date,
                    end_date=strategy.end_date,
                    period=strategy.period,
                    interval=strategy.interval

                )

        if DataCollector.FUNDAMENTALS_KEY in data_sources.keys():
            data_source_fundamentals = data_sources[DataCollector.FUNDAMENTALS_KEY]

            if data_source_fundamentals is not None:
                data_source_fundamentals.extract_fundamentals(
                    tickers=tickers,
                    required_elements=strategy.fundamentals_options)


        indicators = strategy.indicators
        value_investing_metrics = strategy.value_investing_metrics
        stocks = StocksFactory.load_stocks(
            tickers=tickers,
            data_source_historical=data_source_historical,
            data_source_fundamentals=data_source_fundamentals,
            bulk=bulk,
            indicators=indicators,
            value_investing_metrics=value_investing_metrics
        )

        return stocks

    @staticmethod
    def load_stocks(tickers=None,
                    data_source_historical=None,
                    data_source_fundamentals=None,
                    bulk=False,
                    indicators=None,
                    value_investing_metrics=None):

        stocks = []
        if data_source_historical is None and data_source_fundamentals is None:
            print("Error: Define your data sources first !!!.")
            return

        if data_source_historical is not None:
            tickers = tickers

        elif data_source_fundamentals is not None:
            tickers = tickers

        else:
            print("Error: Set Historical data")
            return


        if bulk is True:  # print("This option has not been already programmed! wait for next release")

            stock = Stock(tickers=tickers,
                          data_source_historical=data_source_historical,
                          data_source_fundamentals=data_source_fundamentals)

            stock = StocksFactory.load_indicators(stock, indicators)
            stock = StocksFactory.load_value_investing_metrics(stock, indicators)
            stocks.append(stock)

        else:
            for ticker in tickers:

                data_source_stock = None
                if data_source_historical is not None:
                    data_source_stock = copy.copy(data_source_historical)
                    data_source_stock.prices = pd.DataFrame()

                    data_source_stock.prices = pd.concat([data_source_historical.prices[ticker]], axis=1, keys=[ticker])

                if data_source_fundamentals is not None:
                    data_source_fundamentals_stock = copy.copy(data_source_fundamentals)
                    data_source_fundamentals_stock.fundamentals = copy.copy(data_source_fundamentals.fundamentals)

                    data_source_fundamentals_stock.fundamentals.overview_df = pd.DataFrame()
                    data_source_fundamentals_stock.fundamentals.income_statement_ar_df = pd.DataFrame()
                    data_source_fundamentals_stock.fundamentals.balance_sheet_ar_df = pd.DataFrame()
                    data_source_fundamentals_stock.fundamentals.cashflow_ar_df = pd.DataFrame()

                    data_source_fundamentals_stock.fundamentals.overview_df = pd.concat([data_source_fundamentals.fundamentals.overview_df[ticker]], axis=1, keys=[ticker])
                    data_source_fundamentals_stock.fundamentals.income_statement_ar_df = pd.concat([data_source_fundamentals.fundamentals.income_statement_ar_df[ticker]], axis=1, keys=[ticker])
                    data_source_fundamentals_stock.fundamentals.balance_sheet_ar_df = pd.concat([data_source_fundamentals.fundamentals.balance_sheet_qr_df[ticker]], axis=1, keys=[ticker])
                    data_source_fundamentals_stock.fundamentals.cashflow_ar_df = pd.concat([data_source_fundamentals.fundamentals.cashflow_ar_df[ticker]], axis=1, keys=[ticker])

                else:
                    data_source_fundamentals_stock = None

                stock = Stock(tickers=[ticker],
                              data_source_historical=data_source_stock,
                              data_source_fundamentals=data_source_fundamentals_stock)

                stock = StocksFactory.load_indicators(stock, indicators)
                stock = StocksFactory.load_value_investing_metrics(stock, value_investing_metrics)

                stocks.append(stock)

        return stocks

    @staticmethod
    def load_indicators(stock, indicators):

        if indicators is None:
            indicators = []

        for indicator in indicators:
            stock.append_indicator(copy.copy(indicator))

        return stock


    @staticmethod
    def load_value_investing_metrics(stock, value_investing_metrics):

        if value_investing_metrics is None:
            value_investing_metrics = []

        for metric in value_investing_metrics:
            stock.append_value_investing_metric(copy.copy(metric))

        return stock
