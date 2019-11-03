# ./execution
# python3 Scrapper.py

import requests

from IncomeStatement import IncomeStatement

class Scrapper:

    webpage = None
    src = None
    error = None

    def __init__(self):
        self.load_parameters()


    def get_fundamentals(self):

        self.load_webpage()
        self.extract_data()



    def load_webpage(self):
        if self.webpage is not None:
            self.src = requests.get(self.webpage)

            status_code = self.src.status_code

            #headers = result.headers
            #print(headers)

            if status_code == 200:
                pass
            else:
                #set error and return
                pass
        else:
            #  Set error and return
            pass


    def extract_data(self):

        income_statement = IncomeStatement(self.src)
        income_statement.get_data()


    def load_parameters(self):
        self.webpage = "https://finance.yahoo.com/quote/FB/financials?p=FB"



