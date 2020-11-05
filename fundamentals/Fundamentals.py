from fundamentals.IncomeStatement import IncomeStatement
from fundamentals.BalanceSheet import BalanceSheet
from fundamentals.CashFlow import CashFlow
from fundamentals.Overview import Overview

import pandas as pd


from enum import Enum



class FUNDAMENTALSTYPE(Enum):
    OVERVIEW = 1
    BALANCE_SHEET = 2
    CASH_FLOW = 3
    INCOME_STATEMENT = 4

class Fundamentals:


    def __init__(self, tickers):
        self.error = None
        self.data = {}
        self.overview_df = pd.DataFrame()
        self.balance_sheet_qr_df = pd.DataFrame()
        self.balance_sheet_ar_df = pd.DataFrame()
        self.income_statement_qr_df = pd.DataFrame()
        self.income_statement_ar_df = pd.DataFrame()
        self.cashflow_qr_df = pd.DataFrame()
        self.cashflow_ar_df = pd.DataFrame()

        self.tickers = tickers


    def process_data(self, ticker, type_fundamentals, data):
        if type_fundamentals is FUNDAMENTALSTYPE.OVERVIEW:
            overview = Overview(ticker, data)

            self.overview_df = pd.concat(
                [overview.data, self.overview_df],
                axis=1
            )

        if type_fundamentals is FUNDAMENTALSTYPE.BALANCE_SHEET:
            balance_sheet = BalanceSheet(ticker, data)

            self.balance_sheet_qr_df = pd.concat(
                [balance_sheet.quarterly_reports, self.balance_sheet_qr_df],
                axis=1
            )

            self.balance_sheet_ar_df = pd.concat(
                [balance_sheet.annual_reports, self.balance_sheet_ar_df],
                axis=1
            )
        if type_fundamentals is FUNDAMENTALSTYPE.INCOME_STATEMENT:
            income_statement = IncomeStatement(ticker, data)

            self.income_statement_qr_df = pd.concat(
                [income_statement.quarterly_reports, self.income_statement_qr_df],
                axis=1
            )

            self.income_statement_ar_df = pd.concat(
                [income_statement.annual_reports, self.income_statement_ar_df],
                axis=1
            )

        if type_fundamentals is FUNDAMENTALSTYPE.CASH_FLOW:
            cashflow = CashFlow(ticker, data)

            self.cashflow_qr_df = pd.concat(
                [cashflow.quarterly_reports, self.cashflow_qr_df],
                axis=1
            )

            self.cashflow_ar_df = pd.concat(
                [cashflow.annual_reports, self.cashflow_ar_df],
                axis=1
            )











