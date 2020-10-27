from fundamentals.IncomeStatement import IncomeStatement
from fundamentals.BalanceSheet import BalanceSheet
from fundamentals.CashFlow import CashFlow
from fundamentals.Overview import Overview

import pandas as pd


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
        self.overview_df = pd.DataFrame()


    def process_data(self, type_fundamentals, data):
        if type_fundamentals is FUNDAMENTALSTYPE.OVERVIEW:
            overview = Overview(data)
            self.overview_df.insert(len(self.overview_df.columns),overview.get_ticker(), overview.data[overview.get_ticker()])


        if type_fundamentals is FUNDAMENTALSTYPE.BALANCE_SHEET:
            self.data[FUNDAMENTALSTYPE.BALANCE_SHEET] = BalanceSheet(data)

        if type_fundamentals is FUNDAMENTALSTYPE.INCOME_STATEMENT:
            self.data[FUNDAMENTALSTYPE.INCOME_STATEMENT] = IncomeStatement(data)

        if type_fundamentals is FUNDAMENTALSTYPE.CASH_FLOW:
            self.data[FUNDAMENTALSTYPE.CASH_FLOW] = CashFlow(data)












