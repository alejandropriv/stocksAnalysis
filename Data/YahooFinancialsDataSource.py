from yahoofinancials import YahooFinancials

import pandas as pd

import datetime
import sys

from Data.DataSource import DataSource


class YahooFinancialsDataSource(DataSource):

    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def __init__(self, ticker):
        self.ticker = ticker
        self.end_date = (datetime.date.today()).strftime('%Y-%m-%d')
        self.start_date = (datetime.date.today() - datetime.timedelta(1825)).strftime('%Y-%m-%d')

    # all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "INTC"]

    def extract_historical_data(self):

        self.extract_data()

    def extract_data(self):
        close_prices = pd.DataFrame()

        # extracting stock data (historical close price) for the stocks identified

        attempt = 0
        drop = []
        while attempt <= 5:
            print("-----------------")
            print("attempt number ", attempt)
            print("-----------------")

            try:
                yahoo_financials = YahooFinancials(self.ticker)

                json_obj = yahoo_financials.get_historical_price_data(self.start_date, self.end_date, "daily")
                ohlv = json_obj[self.ticker]['prices']
                temp = pd.DataFrame(ohlv)[["formatted_date", "adjclose"]]
                temp.set_index("formatted_date", inplace=True)
                temp2 = temp[~temp.index.duplicated(keep='first')]
                close_prices[self.ticker] = temp2["adjclose"]
                drop.append(self.ticker)

                print(ohlv)
                break

            except:
                print("Unexpected error:", sys.exc_info())
                print(self.ticker, " :failed to fetch data...retrying")

                continue

            attempt += 1
