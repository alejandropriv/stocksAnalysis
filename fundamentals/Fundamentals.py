from fundamentals.IncomeStatement import IncomeStatement
from fundamentals.BalanceSheet import BalanceSheet
from fundamentals.CashFlow import CashFlow
from fundamentals.Overview import Overview

import pandas as pd

from fundamentals.Statistics import Statistics

from enum import Enum



class FUNDAMENTALSTYPE(Enum):
    OVERVIEW = 1
    BALANCE_SHEET = 2
    CASH_FLOW = 2
    INCOME_STATEMENT = 3

class Fundamentals:


    def __init__(self):
        self.error = None

        self.data = {}


    def process_data(self, type_fundamentals, data):
        if type_fundamentals is FUNDAMENTALSTYPE.OVERVIEW:
            self.data[FUNDAMENTALSTYPE.OVERVIEW] = Overview(dict=data)


    def get_data(self):


        print("\nGetting Fundamentals for:" + self.ticker + " ticker.")

        self.income_statement = IncomeStatement(self.ticker)

        self.balance_sheet = BalanceSheet(self.ticker)

        self.cash_flow = CashFlow(self.ticker)

        self.statistics = Statistics(self.ticker)

        self.clean_data()









