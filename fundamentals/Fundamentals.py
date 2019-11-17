import requests

from fundamentals.IncomeStatement import IncomeStatement
from fundamentals.BalanceSheet import BalanceSheet
from fundamentals.CashFlow import CashFlow
from fundamentals.Statistics import Statistics

import pandas as pd




class Fundamentals:

    error = None

    financial_dir = {}
    income_statement = None
    cash_flow = None
    balance_sheet = None
    statistics = None
    ticker = None



    def __init__(self, ticker):
        self.ticker = ticker

    def acquire_fundamentals(self):


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

        combined_financials = pd.DataFrame(self.financial_dir)
        tickers = combined_financials.columns
        for ticker in tickers:
            combined_financials = combined_financials[~combined_financials[ticker].str.contains("[a-z]").fillna(False)]

        print("WOW")







