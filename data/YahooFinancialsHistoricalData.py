from yahoofinancials import YahooFinancials
from data.HistoricalData import HistoricalData

import pandas as pd
from utilities.Constants import Constants

import datetime
import sys


class YahooFinancialsHistoricalData(HistoricalData):

    def __init__(self):
        super().__init__()
        self.high = pd.DataFrame()
        self.low = pd.DataFrame()
        self.open = pd.DataFrame()
        self.close = pd.DataFrame()
        self.volume = pd.DataFrame()
        self.adj_close = pd.DataFrame()

    # all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "INTC"]
    def extract_historical_data(self,
                                tickers,
                                start_date=(datetime.date.today() - datetime.timedelta(1825)).strftime('%Y-%m-%d'),
                                end_date=datetime.date.today().strftime('%Y-%m-%d'),
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

        # extracting stock data (historical close price) for the stocks identified

        for ticker in self.tickers:

            attempt = 0

            while attempt <= 5:
                print("-------------------------------------")
                print("Ticker: {0} - attempt number:{1} ".format(ticker, attempt))
                print("-------------------------------------")

                try:
                    yahoo_financials = YahooFinancials(ticker)

                    json_obj = yahoo_financials.get_historical_price_data(self.start_date, self.end_date,
                                                                          self.time_series.value)
                    ohlv = json_obj[ticker]['prices']

                    if self.data_columns[0] == "all":
                        temp_adj_close = pd.DataFrame(ohlv)[["formatted_date",
                                                             "adjclose"
                                                             ]]

                        temp_high = pd.DataFrame(ohlv)[["formatted_date",
                                                        "high"
                                                        ]]

                        temp_low = pd.DataFrame(ohlv)[["formatted_date",
                                                       "low"
                                                       ]]

                        temp_open = pd.DataFrame(ohlv)[["formatted_date",
                                                        "open"
                                                        ]]

                        temp_close = pd.DataFrame(ohlv)[["formatted_date",
                                                         "close"
                                                         ]]

                        temp_volume = pd.DataFrame(ohlv)[["formatted_date",
                                                          "volume",
                                                          ]]

                        temp_adj_close.set_index("formatted_date", inplace=True)
                        temp_high.set_index("formatted_date", inplace=True)
                        temp_low.set_index("formatted_date", inplace=True)
                        temp_open.set_index("formatted_date", inplace=True)
                        temp_close.set_index("formatted_date", inplace=True)

                        temp_volume.set_index("formatted_date", inplace=True)

                        temp_adj_close2 = temp_adj_close[~temp_adj_close.index.duplicated(keep='first')]
                        temp_high2 = temp_high[~temp_high.index.duplicated(keep='first')]
                        temp_low2 = temp_low[~temp_low.index.duplicated(keep='first')]
                        temp_open2 = temp_open[~temp_open.index.duplicated(keep='first')]
                        temp_close2 = temp_close[~temp_close.index.duplicated(keep='first')]
                        temp_volume2 = temp_volume[~temp_volume.index.duplicated(keep='first')]


                        self.adj_close[ticker] = temp_adj_close2["adjclose"]
                        self.high[ticker] = temp_high2["high"]
                        self.low[ticker] = temp_low2["low"]
                        self.open[ticker] = temp_open2["open"]
                        self.close[ticker] = temp_close2["close"]
                        self.volume[ticker] = temp_volume2["volume"]

                        print(ohlv)

                    break

                except:
                    print("Unexpected error:", sys.exc_info())
                    print(ticker, " :failed to fetch data...retrying")
                    attempt += 1

                    continue



    def clear_data(self):
        self.adj_close.bfill(axis=0, inplace=True)
        self.high[ticker] = temp_high2["high"]
        self.low[ticker] = temp_low2["low"]
        self.open[ticker] = temp_open2["open"]
        self.close[ticker] = temp_close2["close"]
        self.volume[ticker] = temp_volume2["volume"]