from fundamentals.Fundamentals import Fundamentals

from data.DataSource import DataSource
from data.PandasDataReaderDataSource import PandasDataReaderDataSource
from data.YFinanceDataSource import YFinanceDataSource
from data_analysis.DailyReturn import DailyReturn
from plotter.Plotter import Plotter
from utilities.Constants import Constants

import datetime


class Stock:

    # Put here an enum and a case with the enum
    def __init__(self,
                 tickers=None,
                 data_source=None):

        self.error = None
        self.fundamentals = None
        self.data_source = None
        self.daily_return = None

        self.price_info = None

        self.indicators = []

        if tickers is None:
            print("Error: Define your tickers first !!!.")
            raise ValueError

        self.tickers = tickers



        self.set_data_source(data_source)

        print("Stock {} created".format(tickers))

    def set_data_source(self, data_source):
        if data_source is None:
            print("Error: Please Specify a DataSource object !!!.")
            raise ValueError

        self.data_source = data_source
        self.get_prices_data()




    def get_fundamentals(self):
        self.fundamentals = {}
        for ticker in self.tickers:
            self.fundamentals[ticker] = Fundamentals(ticker)
            self.fundamentals[ticker].get_data()


    def get_prices_info(self, cached=False, tickers=None, keys=None):
        if cached is True:
            return self.price_info
        else:
            return self.get_prices_data(tickers=tickers, keys=keys)


    # Tickers parameter should be a sub-set of self.tickers
    def get_prices_data(self,
                        tickers=None,
                        keys=None):

        if keys is None or len(keys) == 0:
            print("No keys has been specified. All keys were selected. ")

            keys = {'has_high_key': True,
                    'has_low_key': True,
                    'has_open_key': True,
                    'has_close_key': True,
                    'has_adj_close_key': True,
                    'has_volume_key': True
                    }



        method_tag = "get_prices_data"

        if tickers is None:
            print("Default Tickers = ", self.tickers)
            tickers = self.tickers

        if self.data_source is not None:
            if self.data_source.prices is None or self.data_source.prices.empty is True:
                print("No historical data available, call method self.get_historical_data() first")
                raise NotImplementedError  # here there should be an error object

            key_titles = []
            for ticker in tickers:

                if keys["has_high_key"] == True:
                    key = self.data_source.get_high_key(ticker)
                    if key is not None:
                        key_titles.append(key)


                if keys["has_low_key"] == True:
                    key = self.data_source.get_low_key(ticker)
                    if key is not None:
                        key_titles.append(key)


                if keys["has_open_key"] == True:
                    key = self.data_source.get_open_key(ticker)
                    if key is not None:
                        key_titles.append(key)


                if keys["has_close_key"] == True:
                    key = self.data_source.get_close_key(ticker)
                    if key is not None:
                        key_titles.append(key)


                if keys["has_adj_close_key"] == True:
                    key = self.data_source.get_adj_close_key(ticker)
                    if key is not None:
                        key_titles.append(key)

                if keys["has_volume_key"] == True:
                    key = self.data_source.get_volume_key(ticker)
                    if key is not None:
                        key_titles.append(key)



            if len(key_titles) > 0:
                self.data_source.prices = self.data_source.prices.sort_index()
                prices = self.data_source.prices[self.tickers].loc[:, key_titles]


            else:
                print("{} - There are no prices information, for ticker:{}".format(method_tag, self.tickers))
                raise ValueError



        else:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        if prices.empty == True:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        self.price_info = prices
        return prices


    def get_historical_data(self,
                            end_date=datetime.datetime.now(),
                            start_date=None,
                            time_delta=None,
                            period=None,
                            interval=Constants.INTERVAL.DAY):




        if self.data_source.prices is None or self.data_source.prices.empty == True:
            self.data_source.extract_historical_data(
                start_date=start_date,
                end_date=end_date,
                time_delta=time_delta,
                period=period,
                interval=interval)


            self.price_info = self.get_prices_data(tickers=self.tickers)


    # def append_indicator(self, new_indicator=None, keys=None):
    #
    #     if keys is None:
    #         keys = {'has_high_key': True,
    #                 'has_low_key': True,
    #                 'has_open_key': False,
    #                 'has_close_key': False,
    #                 'has_adj_close_key': True,
    #                 'has_volume_key': True
    #                 }
    #
    #     # if get_historical_data has already been called it returns the cached data
    #     self.get_historical_data()
    #
    #     self.price_info = self.get_prices_data(tickers=self.tickers,
    #                                            keys=keys)
    #
    #     self.price_info.ticker = self.tickers[0]
    #
    #
    #     new_indicator.set_input_data(self.price_info)
    #     new_indicator.calculate()
    #
    #     self.indicators.append(new_indicator)




    # def plot(self, ticker=None, price_types=None, period=100):
    #     if price_types is None:
    #         # Initialize price types if no value has been provided
    #         price_types = ["adj_close"]
    #
    #     if ticker is None:
    #         # Initialize ticker value if it has not been provided
    #         ticker = [self.tickers[0]]
    #
    #     if self.plotter is None:
    #         # Initialize Plotter if it has not been already initialized
    #         self.plotter = Plotter()
    #
    #     for priceType in price_types:
    #         if priceType == "adj_close":
    #             keys = {'has_high_key': False,
    #                     'has_low_key': False,
    #                     'has_open_key': False,
    #                     'has_close_key': False,
    #                     'has_adj_close_key': True,
    #                     'has_volume_key': True
    #                     }
    #
    #             self.price_info = self.get_prices_data(ticker, keys=keys)
    #
    #             self.price_info.ticker = ticker[0]
    #             self.plotter.plot_main(df=self.price_info, period=period)  # count how many graphics there will be
    #
    #     for indicator in self.indicators:
    #         indicator.plot(plotter=self.plotter, period=period)






    def get_statistical_data(self, period):
        pass
        # if self.data_source.adj_close is None:
        #     print("Unable to get statistical data because there is no data, calling 'self.get_historical_data()' first")
        #     self.get_historical_data()
        #
        # self.daily_return = DailyReturn(self.get_prices_close_adj(), period)
        # self.daily_return.get_statistical_data()