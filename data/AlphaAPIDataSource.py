from data.DataSource import DataSource
from http_request.HttpRequest import HttpRequest

from fundamentals.Fundamentals import Fundamentals
import pandas as pd

import json

import os

import datetime
import sys
import time

from utilities.Constants import Constants
from pprint import pprint
import traceback

import config



class AlphaAPIDataSource(DataSource):

    _AV_API_URL = "https://www.alphavantage.co/query"
    _FUNCTION = "function"
    _SYMBOL = "symbol"
    _API_KEY = "apikey"
    _AV_API_KEY = "86VFFOKUNB1M9YQ8"

    _QA_API_KEY = False

    def __init__(self, proxy=None):

        super().__init__()

        self.prices = pd.DataFrame()
        self.fundamentals = None


        self.proxy = proxy

        self.url = None

    # Form the base url, the original function called must return
    # the function name defined in the alpha vantage api and the data
    # key for it and for its meta data.
    @staticmethod
    def calculate_url(ticker, function):

        url = "{}?{}={}&{}={}&{}={}".format(
            AlphaAPIDataSource._AV_API_URL,
            AlphaAPIDataSource._FUNCTION,
            function.name,
            AlphaAPIDataSource._SYMBOL,
            ticker,
            AlphaAPIDataSource._API_KEY,
            AlphaAPIDataSource._AV_API_KEY

        )
        print(url)


        return url


    def save_record(self, ticker, element, response):
        data = {'ticker': ticker, 'element': element.value, 'response': response}

        file_path = os.path.join(config.ROOT_DIR, 'data', 'av_cache', '{}_{}.txt'.format(ticker, element))
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)


    def load_cached_data(self, ticker, element):
        file_path = os.path.join(config.ROOT_DIR, 'data', 'av_cache', '{}_{}.txt'.format(ticker, element))
        with open(file_path, 'w') as json_data_file:
            json.load(json_data_file)

    def extract_fundamentals(self, tickers, required_elements=None, force=0):

        num_requests = 1

        if required_elements is None:
            raise ValueError("No fundamentals selected, please check your code")

        self.fundamentals = Fundamentals(tickers)

        for element in required_elements:

            for i in range(0, len(tickers)):
                ticker = tickers[i]
                if ticker.startswith("^"):
                    continue

                if force == 0 or force == 2:
                    self.load_cached_data(ticker, element)



                url = self.calculate_url(ticker, element)
                try:
                    response = \
                        HttpRequest.execute(
                            url=url,
                            proxy=self.proxy,
                            treat_info_as_error=True
                        )
                    self.fundamentals.process_data(ticker, element, response)
                    self.save_record(ticker, element, response)
                    print(response)
                    i += 1

                except Exception:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    pprint(traceback.format_exception(exc_type, exc_value, exc_tb))
                    # TODO: Mirar un timeout o un maximo de excepciones
                    time.sleep(61)

                # TODO: This can be severely optimized and in a thread run and with a production api key
                if num_requests >= 5 and AlphaAPIDataSource._QA_API_KEY is True:
                    time.sleep(61)
                    num_requests = 0

                num_requests += 1

        #print()

    def extract_historical_data(self,
                                tickers=None,
                                start_date=None,
                                end_date=(datetime.date.today()),
                                time_delta=None,
                                period=None,
                                interval=Constants.INTERVAL.DAY):


        pass


    def validate_parameters(self):
        pass


    def get_prices(self, tickers, key_titles):
        pass
