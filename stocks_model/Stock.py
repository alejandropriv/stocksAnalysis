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
        self.interval = None
        self.start_date = None
        self.end_date = None
        self.daily_return = None


        self.indicators = []

        if tickers is None:
            print("Error: Define your tickers first !!!.")
            raise ValueError

        self.tickers = tickers

        if data_source is None:
            print("Error: Please Specify a datasource !!!.")
            raise ValueError

        self.data_source = data_source

        self.price_info = None

        print("Stock {} created".format(tickers))


    def get_fundamentals(self):
        self.fundamentals = {}
        for ticker in self.tickers:
            self.fundamentals[ticker] = Fundamentals(ticker)
            self.fundamentals[ticker].get_data()



    def get_historical_data(self,
                            end_date=datetime.datetime.now(),
                            start_date=None,
                            time_delta=None,
                            period=None,
                            interval=Constants.INTERVAL.DAY):

        self.interval = interval

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


        if self.data_source.prices is None or self.data_source.prices.empty == True:
            self.data_source.extract_historical_data(
                tickers=self.tickers,
                start_date=start_date,
                end_date=end_date,
                period=period,
                interval=interval)


            self.price_info = self.get_prices_data(tickers=self.tickers)


    # Tickers parameter should be a sub-set of self.tickers
    def get_prices_data(self,
                        tickers=None,
                        keys=None ):

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
                    key_titles.append(Constants.get_high_key(ticker))

                if keys["has_low_key"] == True:
                    key_titles.append(Constants.get_low_key(ticker))

                if keys["has_volume_key"] == True:
                    key_titles.append(Constants.get_volume_key(ticker))

                if keys["has_open_key"] == True:
                    key_titles.append(Constants.get_open_key(ticker))

                if keys["has_close_key"] == True:
                    key_titles.append(Constants.get_close_key(ticker))

                if keys["has_adj_close_key"] == True:
                    key_titles.append(Constants.get_adj_close_key(ticker))


            if len(key_titles) > 0:

                prices = self.data_source.prices.loc[:, key_titles]


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



    def append_indicator(self, new_indicator=None, keys=None):

        if keys is None:
            keys = {'has_high_key': True,
                    'has_low_key': True,
                    'has_open_key': False,
                    'has_close_key': False,
                    'has_adj_close_key': True,
                    'has_volume_key': True
                    }

        # if get_historical_data has already been called it returns the cached data
        self.get_historical_data()

        self.price_info = self.get_prices_data(tickers=self.tickers,
                                               keys=keys)

        self.price_info.ticker = self.tickers[0]


        new_indicator.set_input_data(self.price_info)
        new_indicator.calculate()

        self.indicators.append(new_indicator)




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