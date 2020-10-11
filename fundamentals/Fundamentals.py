from fundamentals.IncomeStatement import IncomeStatement
from fundamentals.BalanceSheet import BalanceSheet
from fundamentals.CashFlow import CashFlow
from fundamentals.Statistics import Statistics

from enum import Enum



class FUNDAMENTALSTYPE(Enum):
    OVERVIEW = 1
    BALANCE_SHEET = 2
    CASH_FLOW = 2
    INCOME_STATEMENT = 3

class Fundamentals:


    def __init__(self, ticker):
        self.ticker = ticker
        self.error = None

        self.financial_dir = {}
        self.income_statement = None
        self.cash_flow = None
        self.balance_sheet = None
        self.statistics = None


    def get_data(self):


        print("\nGetting Fundamentals for:" + self.ticker + " ticker.")

        self.income_statement = IncomeStatement(self.ticker)

        self.balance_sheet = BalanceSheet(self.ticker)

        self.cash_flow = CashFlow(self.ticker)

        self.statistics = Statistics(self.ticker)

        self.clean_data()



    def clean_data(self):

        fundamentals = self.income_statement.get_data()
        fundamentals.update(self.balance_sheet.get_data())
        fundamentals.update(self.cash_flow.get_data())
        fundamentals.update(self.statistics.get_data())

        # combining all extracted information with the corresponding ticker
        self.financial_dir[self.ticker] = fundamentals

        # storing information in pandas dataframe

#        combined_financials = pd.DataFrame(self.financial_dir)
#        tickers = combined_financials.columns
#        for ticker in tickers:
#            combined_financials = combined_financials[~combined_financials[ticker].str.contains("[a-z]").fillna(False)]

        print("WOW")







