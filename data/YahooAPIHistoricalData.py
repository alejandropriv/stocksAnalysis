from data.HistoricalData import HistoricalData
import pandas as pd
import pandas_datareader.data as pdr

import sys

import datetime


class YahooAPIHistoricalData(HistoricalData):

    def __init__(self):
        super().__init__()
        self.high = pd.DataFrame()
        self.low = pd.DataFrame()
        self.open = pd.DataFrame()
        self.close = pd.DataFrame()
        self.volume = pd.DataFrame()
        self.adj_close = pd.DataFrame()


    def extract_historical_data(self,
                                tickers,
                                start_date=datetime.date.today() - datetime.timedelta(365),
                                end_date=(datetime.date.today()),
                                time_series=HistoricalData.TIMESERIES.DAILY,
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
        if self.time_series == HistoricalData.TIMESERIES.DAILY:
            interval = 'd'

        elif self.time_series == HistoricalData.TIMESERIES.WEEKLY:
            interval = 'w'

        elif self.time_series == HistoricalData.TIMESERIES.MONTHLY:
            interval = 'm'

        # extracting stock data (historical close price) for the stocks identified
        for ticker in self.tickers:

            attempt = 0

            while attempt <= 5:
                print("-------------------------------------")
                print("Ticker: {0} - attempt number:{1} ".format(ticker, attempt))
                print("-------------------------------------")

                try:
                    temp = pdr.get_data_yahoo(ticker, self.start_date, self.end_date, interval=interval)
                    temp.dropna(inplace=True)

                    # TODO: Validate and put the code to handle different columns
                    if self.data_columns[0] == "all":

                        self.high[ticker] = temp["High"]
                        self.low[ticker] = temp["Low"]
                        self.open[ticker] = temp["Open"]
                        self.close[ticker] = temp["Close"]
                        self.adj_close[ticker] = temp["Adj Close"]

                    print("prices were added for {}".format(ticker))

                    break

                except Exception as why:
                    print("Unexpected error:{}, Why:{}".format(sys.exc_info(), why))
                    print(ticker, " :failed to fetch data...retrying")
                    attempt += 1

                    continue
