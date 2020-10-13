from data.DataSource import DataSource
from http_request.HttpRequest import HttpRequest

from fundamentals.Fundamentals import Fundamentals
import pandas as pd

import datetime

from utilities.Constants import Constants




class AlphaAPIDataSource(DataSource):

    _AV_API_URL = "https://www.alphavantage.co/query"
    _FUNCTION = "function"
    _SYMBOL = "symbol"
    _API_KEY = "apikey"
    _AV_API_KEY = "86VFFOKUNB1M9YQ8"

    def __init__(self,
                 api_key=None,
                 proxy=None
                 ):

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
        #         return "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo"




    def extract_fundamentals(self, tickers, required_elements=None):

        if required_elements is None:
            raise ValueError("No fundamentals selected, please check your code")

        fundamentals = Fundamentals()

        for element in required_elements:



            for ticker in tickers:
                url = self.calculate_url(ticker, element)
                try:
                    response = \
                        HttpRequest.execute(
                            url=url,
                            proxy=self.proxy,
                            treat_info_as_error=True
                        )

                    print(response)
                except Exception as e:
                    print(e)
                # TODO: Mirar que pasa con los retries y los caracteres especiales


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
        # result = self.validate_dates()
        #
        # # Intra-day intervals
        # if self.interval is Constants.INTERVAL.MINUTE or \
        #         self.interval is Constants.INTERVAL.MINUTE2 or \
        #         self.interval is Constants.INTERVAL.MINUTE5 or \
        #         self.interval is Constants.INTERVAL.MINUTE15 or \
        #         self.interval is Constants.INTERVAL.MINUTE30 or \
        #         self.interval is Constants.INTERVAL.MINUTE60 or \
        #         self.interval is Constants.INTERVAL.MINUTE90 or \
        #         self.interval is Constants.INTERVAL.HOUR:
        #
        #     if self.start_date is None and self.end_date is None:
        #
        #         if self.period is not Constants.PERIOD.DAY or \
        #                 self.period is not Constants.PERIOD.DAY5 or \
        #                 self.period is not Constants.PERIOD.MONTH:
        #
        #             print("For Intra-day you have a maximum of 60 days of data, please adjust your dates!")
        #             result = False
        #
        #
        #     else:
        #         delta = (self.end_date - self.start_date).seconds
        #
        #         max_days = 60 * 24 * 60 * 60
        #         if delta > max_days:
        #             print("For Intra-day you have a maximum of 60 days of data, please adjust your dates!")
        #             result = False
        #
        # return result



    def get_prices(self, tickers, key_titles):
        pass


        # function_name, data_key, meta_data_key = func(
        #     self, *args, **kwargs)
        # base_url = AlphaVantage._RAPIDAPI_URL if self.rapidapi else AlphaVantage._ALPHA_VANTAGE_API_URL
        # url = "{}function={}".format(base_url, function_name)
        # for idx, arg_name in enumerate(argspec.args[1:]):
        #     try:
        #         arg_value = args[idx]
        #     except IndexError:
        #         arg_value = used_kwargs[arg_name]
        #     if 'matype' in arg_name and arg_value:
        #         # If the argument name has matype, we gotta map the string
        #         # or the integer
        #         arg_value = self.map_to_matype(arg_value)
        #     if arg_value:
        #         # Discard argument in the url formation if it was set to
        #         # None (in other words, this will call the api with its
        #         # internal defined parameter)
        #         if isinstance(arg_value, tuple) or isinstance(arg_value, list):
        #             # If the argument is given as list, then we have to
        #             # format it, you gotta format it nicely
        #             arg_value = ','.join(arg_value)
        #         url = '{}&{}={}'.format(url, arg_name, arg_value)
        # # Allow the output format to be json or csv (supported by
        # # alphavantage api). Pandas is simply json converted.
        # if 'json' in self.output_format.lower() or 'csv' in self.output_format.lower():
        #     oformat = self.output_format.lower()
        # elif 'pandas' in self.output_format.lower():
        #     oformat = 'json'
        # else:
        #     raise ValueError("Output format: {} not recognized, only json,"
        #                      "pandas and csv are supported".format(
        #         self.output_format.lower()))
        # apikey_parameter = "" if self.rapidapi else "&apikey={}".format(
        #     self.key)
        # if self._append_type:
        #     url = '{}{}&datatype={}'.format(url, apikey_parameter, oformat)
        # else:
        #     url = '{}{}'.format(url, apikey_parameter)
        # return self._handle_api_call(url), data_key, meta_data_key