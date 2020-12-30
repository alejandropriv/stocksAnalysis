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

        folder_path = os.path.join(config.ROOT_DIR, 'data', 'av_cache')
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)


        file_path = os.path.join(folder_path, '{}_{}.txt'.format(ticker, element))
        with open(file_path, 'w') as outfile:
            json.dump(response, outfile)


    def load_cached_data(self, ticker, element):

        file_path = os.path.join(config.ROOT_DIR, 'data', 'av_cache', '{}_{}.txt'.format(ticker, element))
        try:
            with open(file_path, 'r') as json_data_file:
                response = json.load(json_data_file)

        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            pprint(traceback.format_exception(exc_type, exc_value, exc_tb))
            response = None

        return response
        #Todo: return true if successful then if false do an http request to get the data from the server

    def extract_fundamentals(self, tickers, required_elements=None, force_server_data=0):

        num_requests = 1
        fix_data = 0

        if required_elements is None:
            raise ValueError("No fundamentals selected, please check your code")

        self.fundamentals = Fundamentals(tickers)

        for element in required_elements:

            i = 0
            while i < len(tickers):
                ticker = tickers[i]
                if ticker.startswith("^"):
                    i += 1
                    continue

                response = None
                if force_server_data == 0 and fix_data == 0:
                    response = self.load_cached_data(ticker, element)
                    result = self.fundamentals.process_data(ticker, element, response)

                    # This means that the file loaded is not correct and the correct file
                    # should be picked from the server
                    if result is False:
                        fix_data = 1
                        response = None
                        continue

                if response is None:
                    url = self.calculate_url(ticker, element)
                    try:
                        response = \
                            HttpRequest.execute(
                                url=url,
                                proxy=self.proxy,
                                treat_info_as_error=True
                            )

                        self.save_record(ticker, element, response)

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

                    result = self.fundamentals.process_data(ticker, element, response)


                print(response)

                i += 1
                fix_data = 0


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
