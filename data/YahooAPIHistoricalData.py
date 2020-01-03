from data.HistoricalData import HistoricalData
import pandas as pd
import pandas_datareader.data as pdr
from utilities.Constants import Constants

import sys

import datetime


class YahooAPIHistoricalData(HistoricalData):

    def __init__(self):
        super().__init__()
        self.prices = pd.DataFrame()


    def extract_historical_data(self,
                                tickers,
                                start_date=datetime.date.today() - datetime.timedelta(365),
                                end_date=(datetime.date.today()),
                                time_series=Constants.TIMESERIES.DAILY,
                                data_columns=None):

        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.time_series = time_series

        if data_columns is None:
            data_columns = ["all"]

        self.data_columns = data_columns

        self.extract_data()




    def extract_data(self):

        interval = ""
        if self.time_series == Constants.TIMESERIES.DAILY:
            interval = 'd'

        elif self.time_series == Constants.TIMESERIES.WEEKLY:
            interval = 'w'

        elif self.time_series == Constants.TIMESERIES.MONTHLY:
            interval = 'm'

        # extracting stock data (historical close price) for the stocks identified
        for ticker in self.tickers:

            attempt = 0

            high_key = Constants.get_high_key(ticker)
            low_key = Constants.get_low_key(ticker)
            open_key = Constants.get_open_key(ticker)
            close_key = Constants.get_close_key(ticker)
            adj_close_key = Constants.get_adj_close_key(ticker)
            volume_key = Constants.get_volume_key(ticker)

            while attempt <= 5:
                print("-------------------------------------")
                print("Ticker: {0} - attempt number:{1} ".format(ticker, attempt))
                print("-------------------------------------")

                try:
                    temp = pdr.get_data_yahoo(ticker, self.start_date, self.end_date, interval=interval)

                    print("Ticker: {0} - data received! ".format(ticker))

                    temp.dropna(inplace=True)


                    # TODO: Validate and put the code to handle different columns
                    if self.data_columns[0] == "all":

                        self.prices[high_key] = temp["High"]
                        self.prices[low_key] = temp["Low"]
                        self.prices[open_key] = temp["Open"]
                        self.prices[close_key] = temp["Close"]
                        self.prices[adj_close_key] = temp["Adj Close"]
                        self.prices[volume_key] = temp["Volume"]

                    break


                except Exception as why:
                    print("Unexpected error:{}, Why:{}".format(sys.exc_info(), why))
                    print(ticker, " :failed to fetch data...retrying")
                    attempt += 1

                    continue


        self.prices.bfill(axis=0, inplace=True)
