from fundamentals.Fundamentals import Fundamentals
from data.YahooAPIHistoricalData import YahooAPIHistoricalData
from data.YahooFinancialsHistoricalData import YahooFinancialsHistoricalData
from data_analysis.DailyReturn import DailyReturn
from plotter.Plotter import Plotter
from utilities.Constants import Constants

import datetime


class Stock:

    # Put here an enum and a case with the enum
    def __init__(self, tickers=None, data_source=None, plotter=None):

        self.error = None
        self.fundamentals = None
        self.tickers = None
        self.data_source = None
        self.time_series = None
        self.daily_return = None

        self.indicators = []

        if tickers is None:
            raise ValueError

        if data_source is None:
            data_source = YahooAPIHistoricalData()

        self.price_info = None

        print("Stock {} created".format(tickers))
        self.tickers = tickers
        self.data_source = data_source
        self.plotter = plotter

    def set_data_source(self, data_source_type):
        if data_source_type == YahooAPIHistoricalData.DATASOURCETYPE.YAHOOFINANCIALS:
            self.data_source = YahooFinancialsHistoricalData()

        if data_source_type == YahooAPIHistoricalData.DATASOURCETYPE.YAHOOAPI:
            self.data_source = YahooAPIHistoricalData()

    def get_fundamentals(self):
        self.fundamentals = {}
        for ticker in self.tickers:
            self.fundamentals[ticker] = Fundamentals(ticker)
            self.fundamentals[ticker].get_data()

    def get_historical_data(self,
                            start_date=datetime.date.today() - datetime.timedelta(365),
                            end_date=(datetime.date.today()),
                            time_series=Constants.TIMESERIES.DAILY):

        if self.data_source.prices is None or self.data_source.prices.empty == True:
            self.data_source.extract_historical_data(self.tickers, start_date, end_date, time_series)

    def get_statistical_data(self, period):
        pass
        # if self.data_source.adj_close is None:
        #     print("Unable to get statistical data because there is no data, calling 'self.get_historical_data()' first")
        #     self.get_historical_data()
        #
        # self.daily_return = DailyReturn(self.get_prices_close_adj(), period)
        # self.daily_return.get_statistical_data()

    # Tickers parameter should be a sub-set of self.tickers
    def get_prices_data(self,
                        tickers=None,
                        has_high_key=False,
                        has_low_key=False,
                        has_adj_close_key=False,
                        has_volume_key=False):  # TODO: fix this to be prettier

        method_tag = "get_prices_data"

        if tickers is None:
            print("Default Tickers = ", self.tickers)
            tickers = self.tickers

        if self.data_source is not None:
            if self.data_source.prices is None or self.data_source.prices.empty is True:
                print("No historical data available, call method self.get_historical_data() first")
                raise NotImplementedError  # here there should be an error object

            keys = []

            for ticker in tickers:
                if has_adj_close_key == True:
                    keys.append(Constants.get_adj_close_key(ticker))

                if has_high_key == True:
                    keys.append(Constants.get_high_key(ticker))

                if has_low_key == True:
                    keys.append(Constants.get_low_key(ticker))

                if has_volume_key == True:
                    keys.append(Constants.get_volume_key(ticker))

            if len(keys) > 0:

                prices = self.data_source.prices.loc[:, keys]


            else:
                print("{} - There are no prices information, for ticker:{}".format(method_tag, self.tickers))
                raise ValueError



        else:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        if prices.empty == True:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        return prices

    def append_indicator(self, new_indicator=None, ticker=None):

        # if get_historical_data has already been called it returns the cached data
        self.get_historical_data()

        self.price_info = self.get_prices_data(tickers=self.tickers,
                                               has_high_key=True,
                                               has_low_key=True,
                                               has_adj_close_key=True,
                                               has_volume_key=True)

        if ticker is None:
            self.price_info.ticker = self.tickers[0]
        else:
            # TODO check here for multiple tickers
            self.price_info.ticker = self.tickers[0]

        new_indicator.set_input_data(self.price_info)
        new_indicator.calculate()

        self.indicators.append(new_indicator)






    def plot(self, ticker=None, price_types=None, period=100):
        if price_types is None:
            price_types = ["adj_close"]

        if ticker is None:
            ticker = [self.tickers[0]]

        if self.plotter is None:
            self.plotter = Plotter()

        for priceType in price_types:
            if priceType == "adj_close":
                self.price_info = self.get_prices_data(ticker, has_adj_close_key=True, has_volume_key=True)

                self.price_info.ticker = ticker[0]
                self.plotter.plot_main(df=self.price_info, period=period)  # count how many graphics there will be

        for indicator in self.indicators:
            indicator.plot(plotter=self.plotter, period=period)
