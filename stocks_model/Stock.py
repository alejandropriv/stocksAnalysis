from fundamentals.Fundamentals import Fundamentals

from utilities.Constants import Constants


class Stock:

    # Put here an enum and a case with the enum
    def __init__(self,
                 ticker=None,
                 data_source_historical=None,
                 data_source_fundamentals=None):

        if ticker is None:
            print("Error: Define your tickers first !!!.")
            raise ValueError

        self.ticker = ticker

        self.error = None
        self.fundamentals = None
        self.data_source_historical = data_source_historical

        self.daily_return = None

        self.price_info = None

        self.indicators = []

        if data_source_historical is not None:
            self.get_prices_data()

        self.data_source_fundamentals = data_source_fundamentals
        if data_source_fundamentals is not None:
            self.get_fundamentals()





        print("Stock {} created".format(ticker))




    def get_fundamentals(self):
        self.fundamentals = {self.ticker: Fundamentals(self.ticker)}
        self.fundamentals[self.ticker].get_data()


    def get_key_titles(self, keys):

        key_titles=[]
        if keys["has_high_key"] == True:
            key = Constants.get_high_key()
            if key is not None:
                key_titles.append(key)

        if keys["has_low_key"] == True:
            key = Constants.get_low_key()
            if key is not None:
                key_titles.append(key)

        if keys["has_open_key"] == True:
            key = Constants.get_open_key()
            if key is not None:
                key_titles.append(key)

        if keys["has_close_key"] == True:
            key = Constants.get_close_key()
            if key is not None:
                key_titles.append(key)

        if keys["has_adj_close_key"] == True:
            key = Constants.get_adj_close_key()
            if key is not None:
                key_titles.append(key)

        if keys["has_volume_key"] == True:
            key = Constants.get_volume_key()
            if key is not None:
                key_titles.append(key)

        return key_titles



    # Tickers parameter should be a sub-set of self.tickers
    def get_prices_data(self,
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


        if self.data_source_historical is not None:
            if self.data_source_historical.prices is None or self.data_source_historical.prices.empty is True:
                print("No historical data available, call method self.get_historical_data() first")
                raise NotImplementedError  # here there should be an error object

            key_titles = self.get_key_titles(keys)


            if len(key_titles) > 0:

                # self.data_source.prices = self.data_source.prices.sort_index()
                prices = self.data_source_historical.get_prices(self.ticker, key_titles)


            else:
                print("{} - There are no prices information, for ticker:{}".format(method_tag, self.ticker))
                raise ValueError



        else:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        # Validate Price dataframe
        if prices.empty == True:
            print("There has been an error in {}".format(method_tag))
            raise ValueError


        self.price_info = prices
        return prices



    def append_indicator(self, new_indicator=None):

        # if get_historical_data has already been called it returns the cached data
        new_indicator.set_input_data(self.price_info)
        new_indicator.calculate()

        self.indicators.append(new_indicator)




    def get_statistical_data(self, period):
        pass
        # if self.data_source.adj_close is None:
        #     print("Unable to get statistical data because there is no data, calling 'self.get_historical_data()' first")
        #     self.get_historical_data()
        #
        # self.daily_return = DailyReturn(self.get_prices_close_adj(), period)
        # self.daily_return.get_statistical_data()

    # def get_historical_data(self,
    #                         end_date=datetime.datetime.now(),
    #                         start_date=None,
    #                         time_delta=None,
    #                         period=None,
    #                         interval=Constants.INTERVAL.DAY):
    #
    #
    #
    #
    #     if self.data_source.prices is None or self.data_source.prices.empty == True:
    #         self.data_source.extract_historical_data(
    #             start_date=start_date,
    #             end_date=end_date,
    #             time_delta=time_delta,
    #             period=period,
    #             interval=interval)
    #
    #     self.price_info = self.get_prices_data()