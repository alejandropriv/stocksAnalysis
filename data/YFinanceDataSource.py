from data.DataSource import DataSource
import pandas as pd
import yfinance as yf

import datetime

from utilities.Constants import Constants


class YFinanceDataSource(DataSource):

    def __init__(self, tickers):
        super().__init__(tickers)
        self.prices = pd.DataFrame()

    def extract_historical_data(self,
                                start_date=None,
                                end_date=(datetime.date.today()),
                                time_delta=None,
                                period=None,
                                interval=Constants.INTERVAL.DAY):


        super().extract_historical_data(
            start_date=start_date,
            end_date=end_date,
            period=period,
            interval=interval
        )

        self.start_date = start_date
        self.end_date = end_date
        self.time_delta = time_delta
        self.period = period
        self.interval = interval
        self.interval_str = interval.name




        if self.validate_parameters() is True:
            self.extract_data()

        else:
            print("Verify parameters according to logs")


    def validate_dates(self):

        if self.end_date is None:
            print("Error: end_date is None, Set a valid end date.")
            return False

        if self.period is None and self.start_date is None:
            print("Error: Please set start_date or period")
            return False


        if self.period is None:
            self.period = "max"
        else:
            self.start_date = None
            self.end_date = None


        if self.start_date is not None:
            if self.start_date > self.end_date:

                print("Error:  Start_date should be earlier than end date")
                return False


        elif self.time_delta is not None and self.time_delta > 0:
            self.start_date = datetime.datetime.today() - datetime.timedelta(self.time_delta)


        else:
            print("Error: Neither the Start_date nor the time_delta were defined ")
            return False

        return True



    def validate_parameters(self):

        result = self.validate_dates()

        # Intra-day intervals
        if self.interval is Constants.INTERVAL.MINUTE or \
                self.interval is Constants.INTERVAL.MINUTE2 or \
                self.interval is Constants.INTERVAL.MINUTE5 or \
                self.interval is Constants.INTERVAL.MINUTE15 or \
                self.interval is Constants.INTERVAL.MINUTE30 or \
                self.interval is Constants.INTERVAL.MINUTE60 or \
                self.interval is Constants.INTERVAL.MINUTE90 or \
                self.interval is Constants.INTERVAL.HOUR:

            if self.start_date is None and self.end_date is None:

                if self.period is not Constants.PERIOD.DAY or \
                        self.period is not Constants.PERIOD.DAY5 or \
                        self.period is not Constants.PERIOD.MONTH:

                    print("For Intra-day you have a maximum of 60 days of data, please adjust your dates!")
                    result = False


            else:
                delta = (self.end_date - self.start_date).seconds

                max_days = 60 * 24 * 60 * 60
                if delta > max_days:
                    print("For Intra-day you have a maximum of 60 days of data, please adjust your dates!")
                    result = False

        return result

    def extract_data(self):

        #self.tickers_str = "TSLA SPY"

        self.prices = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers=self.tickers_str,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period=self.period,

            start=self.start_date,

            end=self.end_date,

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval=self.interval.value,

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by='ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust=True,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost=True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads=True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy=None
        )


        self.prices.dropna(inplace=True)

        self.prices.bfill(axis=0, inplace=True)

#TODO put a debug flag for this print
        #print(self.prices)


    def get_high_key(self, ticker):
        key = "{}".format( "High")
        return key

    def get_low_key(self, ticker):
        key = "{}".format("Low")
        return key

    def get_open_key(self, ticker):
        key = "{}".format("Open")
        return key

    def get_close_key(self, ticker):
        key = "{}".format("Close")
        return key

    def get_adj_close_key(self, ticker):
        return None

    def get_volume_key(self, ticker):
        key = "{}".format("Volume")
        return key
