from data.DataSource import DataSource
import pandas as pd
import yfinance as yf

import datetime

from utilities.Constants import Constants


class YFinanceDataSource(DataSource):

    def __init__(self):
        super().__init__()
        self.prices = pd.DataFrame()

    def extract_historical_data(self,
                                tickers,
                                start_date=datetime.date.today() - datetime.timedelta(365),
                                end_date=(datetime.date.today()),
                                period=None,
                                interval=Constants.INTERVAL.DAY):

        super().extract_historical_data(tickers,
                                        start_date=start_date,
                                        end_date=end_date,
                                        period=period,
                                        interval=interval)

        self.tickers = tickers
        self.tickers_str = self.get_tickers_str()


        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.interval = interval
        self.interval_str = interval.name

        if self.period is not None:
            self.start_date = None
            self.end_date = None


        self.validate_parameters()

        self.extract_data()


    def validate_parameters(self):
        if self.interval is Constants.INTERVAL.MINUTE and \
                self.interval is Constants.INTERVAL.MINUTE2 and \
                self.interval is Constants.INTERVAL.MINUTE5 and \
                self.interval is Constants.INTERVAL.MINUTE15 and \
                self.interval is Constants.INTERVAL.MINUTE30 and \
                self.interval is Constants.INTERVAL.MINUTE60 and \
                self.interval is Constants.INTERVAL.MINUTE90 and \
                self.interval is Constants.INTERVAL.HOUR:

            if self.start_date is None or self.end_date is None:

                if self.period is not Constants.PERIOD.DAY or \
                        self.period is not Constants.PERIOD.DAY or \
                        self.period is not Constants.PERIOD.DAY5 or \
                        self.period is not Constants.PERIOD.MONTH:

                    print("For Intra-day you have a maximum of 60 days of data, please adjust your dates!")
                    raise AttributeError


            else:
                delta = (self.end_date - self.start_date).seconds

                max_days = 60 * 24 * 60 * 60
                if delta > max_days:
                    print("For Intra-day you have a maximum of 60 days of data, please adjust your dates!")
                    raise AttributeError



    def get_tickers_str(self):

        tickers_str = ""
        for ticker in self.tickers:
            tickers_str = tickers_str + " " + ticker

        return tickers_str

    def extract_data(self):

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
            interval="1d",

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
            threads=False,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy=None
        )

        self.prices.dropna(inplace=True)

        self.prices.bfill(axis=0, inplace=True)

        print(self.prices)
