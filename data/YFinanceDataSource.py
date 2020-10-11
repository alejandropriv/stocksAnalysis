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
            time_delta=time_delta,
            period=period,
            interval=interval
        )


        if self.validate_parameters() is True:

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


        else:
            print("Verify parameters according to logs")


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



    def extract_fundamentals(self):
        pass

    def get_prices(self, tickers, key_titles):
        available_titles = [Constants.get_open_key(),
                            Constants.get_close_key(),
                            Constants.get_high_key(),
                            Constants.get_low_key(),
                            Constants.get_volume_key()]


        search_titles = []
        for key_title in key_titles:
            if key_title in available_titles:
                search_titles.append(key_title)

        if len(search_titles) == 0:
            print("No valid keys were requested returning empty dataframe")
            return pd.DataFrame()

        # prices_temp = self.prices.copy()
        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in tickers:
            df_list.append(pd.concat([self.prices[ticker].loc[:, search_titles], prices_temp], axis=1, keys=[ticker]))

        prices_temp = pd.concat(
            df_list,
            axis=1
        )


        self.prices = prices_temp.copy()
        return self.prices
