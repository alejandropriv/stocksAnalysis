from data.DataSource import DataSource
from http_request.HttpRequest import HttpRequest

from fundamentals.Fundamentals import Fundamentals
import pandas as pd

import datetime
import sys
import time

from utilities.Constants import Constants
from pprint import pprint
import traceback



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



    def extract_fundamentals(self, tickers, required_elements=None):

        num_requests = 1

        if required_elements is None:
            raise ValueError("No fundamentals selected, please check your code")

        self.fundamentals = Fundamentals(tickers)

        for element in required_elements:

            for ticker in tickers:
                if ticker.startswith("^"):
                    continue

                url = self.calculate_url(ticker, element)
                try:
                    response = \
                        HttpRequest.execute(
                            url=url,
                            proxy=self.proxy,
                            treat_info_as_error=True
                        )
                    self.fundamentals.process_data(ticker, element, response)
                    print(response)

                except Exception:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    pprint(traceback.format_exception(exc_type, exc_value, exc_tb))
                    # TODO: Mirar que pasa con los retries y los caracteres especiales
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
