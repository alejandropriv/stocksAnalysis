# ./execution
# python3 Scrapper.py

import requests

from fundamentals.IncomeStatement import IncomeStatement
from fundamentals.BalanceSheet import BalanceSheet

class Scrapper:

    error = None

    def __init__(self):
        pass

    def get_fundamentals(self):


        self.extract_income_statement()

        self.extract_balance_sheet()



    def load_webpage(self, webpage):
        if webpage is not None:
            src = requests.get(webpage)

            status_code = src.status_code

            #headers = result.headers
            #print(headers)


            if status_code == 200:
                return src

            else:
                #set error and return
                return None
        else:
            #  Set error and return
            raise Exception("Errror Error")


    def extract_income_statement(self):

        webpage = "https://finance.yahoo.com/quote/FB/financials?p=FB"

        src = self.load_webpage(webpage)
        income_statement = IncomeStatement(src)
        income_statement.get_data()


    def extract_balance_sheet(self):

        webpage = "https://finance.yahoo.com/quote/FB/balance-sheet?p=FB"
        src = self.load_webpage(webpage)

        balance_sheet = BalanceSheet(src)
        balance_sheet.get_data()

