from data.DataSource import DataSource


from data.PandasDataReaderDataSource import PandasDataReaderDataSource
from data.YFinanceDataSource import YFinanceDataSource
from utilities.Constants import Constants

import datetime


class StocksFactory:

    # Put here an enum and a case with the enum
    def __init__(self,
                 tickers=None,
                 end_date=datetime.datetime.now(),
                 start_date=None,
                 time_delta= None,
                 time_series=Constants.INTERVAL.DAY,
                 data_source_type=DataSource.DATASOURCETYPE.YFINANCE,
                 bulk=False,
                 group=1):

        self.bulk = bulk
        self.group = group

        if tickers is None:
            print("Error: Define your tickers first !!!.")
            return

        self.tickers = tickers
        print("Tickers for: {} created".format(self.tickers))

        self.data_source = None
        self.set_data_source(data_source_type)

        self.time_series = time_series

        self.end_date = end_date

        self.start_date = None


        if start_date is not None:
            self.start_date = start_date

        elif time_delta is not None:
            self.start_date = datetime.date.today() - datetime.timedelta(time_delta)

        else:
            print("Error: Neither the Start_date nor the time_delta were defined ")
            return
            #TODO: Put here a default interval per timeSeries



        self.stocks = []

        self.bulk = bulk
        self.group = group


    def set_data_source(self, data_source_type):
        if data_source_type is DataSource.DATASOURCETYPE.PANDASDATAREADER:
            self.data_source = PandasDataReaderDataSource()

        elif data_source_type is DataSource.DATASOURCETYPE.YFINANCE:
            self.data_source = YFinanceDataSource

        elif data_source_type is DataSource.DATASOURCETYPE.ALPHA:
            self.data_source = None  #TODO

        elif data_source_type is DataSource.DATASOURCETYPE.YAHOOFINANCIALS:
            self.data_source = None  #TODO


    def createStocks(self):
        if self.tickers is None:
            print("Error: Define your tickers first !!!.")
            return

        if self.start_date is None:
            print("Error: Define a startDate or a timeDelta.")
            return

        if self.bulk is False:

            print("This option has not been already programmed! wait for next release")
            self.data_source.extract_historical_data(ticker=self.tickers,
                                                     start_date=self.start_date,
                                                     end_date=self.end_date,
                                                     interval=self.time_series,
                                                     data_columns=None)

        else:
            for ticker in self.tickers:
                self.data_source.extract_historical_data(ticker=ticker,
                                                         start_date=self.start_date,
                                                         end_date=self.end_date,
                                                         interval=self.time_series,
                                                         data_columns=None)




    def get_historical_data(self,
                            start_date=datetime.date.today() - datetime.timedelta(365),
                            end_date=(datetime.date.today()),
                            time_series=Constants.INTERVAL.DAY):

        if self.data_source.prices is None or self.data_source.prices.empty == True:
            self.data_source.extract_historical_data(self.tickers, start_date, end_date, time_series)



    # Tickers parameter should be a sub-set of self.tickers
    def get_prices_data(self,
                        tickers=None,
                        keys=None ):

        if keys is None:
            print ("No keys has been specified. ")
            raise ValueError

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

