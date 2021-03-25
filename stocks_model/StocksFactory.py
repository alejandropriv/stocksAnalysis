from stocks_model.Stock import Stock

from data.DataCollector import DataCollector

import pandas as pd
import copy

from utilities.Constants import Constants as Ct



class StocksFactory:

    # TODO: Fix this: It was created to fix the problem of having only one stock (input dataframe is different)
    # This should be removed and dataframe handled accordingly
    @staticmethod
    def add_spi500_ticker(tickers):
        tickers.append("^GSPC")
        return tickers

    @staticmethod
    def create_stocks(conf):

        tickers=conf[Ct.tickers_key()]

        data_source_historical = None
        data_source_fundamentals = None

        data_sources = \
            DataCollector.get_data_sources(
                conf[Ct.historical_type_key()],
                conf[Ct.fundamentals_type_key()]
            )

        if DataCollector.HISTORICAL_KEY in data_sources.keys():
            data_source_historical = data_sources[DataCollector.HISTORICAL_KEY]

            if data_source_historical is not None:
                data_source_historical.extract_historical_data(
                    tickers=tickers,
                    start_date=conf[Ct.start_date_key()],
                    end_date=conf[Ct.end_date_key()],
                    period=conf[Ct.period_key()],
                    interval=conf[Ct.interval_key()]

                )

        if DataCollector.FUNDAMENTALS_KEY in data_sources.keys():
            data_source_fundamentals = data_sources[DataCollector.FUNDAMENTALS_KEY]

            if data_source_fundamentals is not None:
                data_source_fundamentals.extract_fundamentals(
                    tickers=tickers,
                    date=conf[Ct.start_date_key],
                    required_elements=conf[Ct.fundamentals_options_key()],
                    force_server_data=conf[Ct.force_fundamentals_key()]
                )

        stocks = StocksFactory.load_stocks(
            tickers=tickers,
            data_source_historical=data_source_historical,
            data_source_fundamentals=data_source_fundamentals,
            bulk=conf[Ct.bulk_key()],
            indicators=conf[Ct.indicators_key()]
        )

        return stocks

    @staticmethod
    def load_stocks(tickers=None,
                    data_source_historical=None,
                    data_source_fundamentals=None,
                    bulk=False,
                    indicators=None
                    ):

        stocks = []
        if data_source_historical is None and data_source_fundamentals is None:
            print("Error: Define your data sources first !!!.")
            return

        if bulk is True:  # print("This option has not been already programmed! wait for next release")

            stock = Stock(tickers=tickers,
                          data_source_historical=data_source_historical,
                          data_source_fundamentals=data_source_fundamentals)

            stock = StocksFactory.load_indicators(stock, indicators)
            stocks.append(stock)

        else:
            for ticker in tickers:

                if ticker.startswith("^"):
                    continue

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

                    data_source_fundamentals_stock.fundamentals.overview_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.overview_df, ticker)

                    data_source_fundamentals_stock.fundamentals.balance_sheet_ar_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.balance_sheet_ar_df,
                                                        ticker)

                    data_source_fundamentals_stock.fundamentals.balance_sheet_qr_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.balance_sheet_qr_df,
                                                        ticker)

                    data_source_fundamentals_stock.fundamentals.income_statement_ar_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.income_statement_ar_df,
                                                        ticker)

                    data_source_fundamentals_stock.fundamentals.income_statement_qr_df = \
                        StocksFactory.set_df_per_ticker(
                            data_source_fundamentals_stock.fundamentals.income_statement_qr_df, ticker)

                    data_source_fundamentals_stock.fundamentals.cashflow_ar_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.cashflow_ar_df, ticker)

                    data_source_fundamentals_stock.fundamentals.cashflow_qr_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.cashflow_qr_df, ticker)

                else:
                    data_source_fundamentals_stock = None

                stock = Stock(tickers=[ticker],
                              data_source_historical=data_source_stock,
                              data_source_fundamentals=data_source_fundamentals_stock)

                stock = StocksFactory.load_indicators(stock, indicators)

                stocks.append(stock)

        return stocks

    @staticmethod
    def set_df_per_ticker(df, ticker):
        if df is not None:
            return pd.concat([df[ticker]], axis=1, keys=[ticker])

    @staticmethod
    def load_indicators(stock, indicators):

        if indicators is None:
            indicators = []

        for indicator in indicators:
            stock.append_indicator(indicator)

        return stock
