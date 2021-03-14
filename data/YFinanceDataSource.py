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
                                tickers=None,
                                start_date=None,
                                end_date=(datetime.date.today()),
                                period=None,
                                interval=Constants.INTERVAL.DAY,
                                time_delta=None
                                ):


        super().extract_historical_data(
            tickers=tickers,
            start_date=start_date,
            end_date=end_date,
            time_delta=time_delta,
            period=period,
            interval=interval
        )

        valid_parameters =\
            YFinanceDataSource.validate_parameters(
                start_date=start_date,
                end_date=end_date,
                time_delta=time_delta,
                period=period,
                interval=interval
            )

        if valid_parameters is False:
            raise ValueError("The proposed dates are not correct, Verify your code!!!")


        tickers_str = self.get_tickers_str(tickers)
        self.prices = yf.download(  # or pdr.get_data_yahoo(...
                # tickers list or string as well
                tickers=tickers_str,

                # use "period" instead of start/end
                # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                # (optional, default is '1mo')
                period=period,

                start=start_date,

                end=end_date,

                # fetch data by interval (including intraday if period < 60 days)
                # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                # (optional, default is '1d')
                interval=interval.value,

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
        self.prices.dropna(axis='columns', how="all", inplace=True)
        self.prices.dropna(axis='rows', how="all", inplace=True)

        self.prices.bfill(axis=0, inplace=True)

        return self.prices

    @staticmethod
    def validate_parameters(start_date=None,
                            end_date=datetime.date.today(),
                            time_delta=None,
                            period=None,
                            interval=None):

        dates = {"start_date":start_date,
                 "end_date":end_date,
                 "time_delta":time_delta,
                 "period":period,
                 "error": None}

        result = \
            DataSource.validate_dates(dates)


        # Intra-day intervals
        if interval is Constants.INTERVAL.MINUTE or \
                interval is Constants.INTERVAL.MINUTE2 or \
                interval is Constants.INTERVAL.MINUTE5 or \
                interval is Constants.INTERVAL.MINUTE15 or \
                interval is Constants.INTERVAL.MINUTE30 or \
                interval is Constants.INTERVAL.MINUTE60 or \
                interval is Constants.INTERVAL.MINUTE90 or \
                interval is Constants.INTERVAL.HOUR:

            if start_date is None and end_date is None:

                if period is not Constants.PERIOD.DAY or \
                        period is not Constants.PERIOD.DAY5 or \
                        period is not Constants.PERIOD.MONTH:

                    print("For Intra-day you have a maximum of 60 days of data, please adjust your dates!")
                    result = False


            else:
                delta = (end_date - start_date).seconds

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
