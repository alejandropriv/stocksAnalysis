import requests

from fundamentals.IncomeStatement import IncomeStatement
from fundamentals.BalanceSheet import BalanceSheet
from fundamentals.CashFlow import CashFlow
from fundamentals.Statistics import Statistics



class Scrapper:

    error = None
    stock_list = []

    def __init__(self, ticker_list):
        self.ticker_list = ticker_list

    def get_fundamentals(self):

        for ticker in self.ticker_list:
            print("\nScrapping " + ticker + " ticker.")

            webpage = "https://finance.yahoo.com/quote/"+ticker+"/financials?p="+ticker
            self.extract_income_statement(webpage)

            webpage = "https://finance.yahoo.com/quote/"+ticker+"/balance-sheet?p="+ticker
            self.extract_balance_sheet(webpage)

            webpage = "https://finance.yahoo.com/quote/"+ticker+"/cash-flow?p="+ticker
            self.extract_cash_flow(webpage)

            webpage = "https://finance.yahoo.com/quote/"+ticker+"/key-statistics?p="+ticker
            self.extract_statistics(webpage)



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


    def extract_income_statement(self, webpage):

        src = self.load_webpage(webpage)
        income_statement = IncomeStatement(src)
        print(income_statement.get_data())


    def extract_balance_sheet(self, webpage):

        src = self.load_webpage(webpage)

        balance_sheet = BalanceSheet(src)
        print(balance_sheet.get_data())


    def extract_cash_flow(self, webpage):
        src = self.load_webpage(webpage)

        cash_flow = CashFlow(src)
        print(cash_flow.get_data())


    def extract_statistics(self, webpage):
        src = self.load_webpage(webpage)

        statistics = Statistics(src)
        item = statistics.get_data()
        print(item)



