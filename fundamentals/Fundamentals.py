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


    def __init__(self):
        self.error = None
        self.data = {}
        self.overview_df = pd.DataFrame()
        self.bs_quarterly_report_df = pd.DataFrame()
        self.bs_annual_report_df = pd.DataFrame()
        self.is_quarterly_report_df = pd.DataFrame()
        self.is_annual_report_df = pd.DataFrame()
        self.cf_quarterly_report_df = pd.DataFrame()
        self.cf_annual_report_df = pd.DataFrame()


    def process_data(self, ticker, type_fundamentals, data):
        if type_fundamentals is FUNDAMENTALSTYPE.OVERVIEW:
            overview = Overview(ticker, data)

            self.overview_df = pd.concat(
                [overview.data, self.overview_df],
                axis=1
            )

        if type_fundamentals is FUNDAMENTALSTYPE.BALANCE_SHEET:
            balance_sheet = BalanceSheet(ticker, data)

            self.bs_quarterly_report_df = pd.concat(
                [balance_sheet.quarterly_reports, self.bs_quarterly_report_df],
                axis=1
            )

            self.bs_annual_report_df = pd.concat(
                [balance_sheet.annual_reports, self.bs_annual_report_df],
                axis=1
            )
        if type_fundamentals is FUNDAMENTALSTYPE.INCOME_STATEMENT:
            self.data[FUNDAMENTALSTYPE.INCOME_STATEMENT] = IncomeStatement(data)
            income_statement = IncomeStatement(ticker, data)

            self.is_quarterly_report_df = pd.concat(
                [income_statement.quarterly_reports, self.is_quarterly_report_df],
                axis=1
            )

            self.is_annual_report_df = pd.concat(
                [income_statement.annual_reports, self.is_annual_report_df],
                axis=1
            )

        if type_fundamentals is FUNDAMENTALSTYPE.CASH_FLOW:
            self.data[FUNDAMENTALSTYPE.CASH_FLOW] = CashFlow(data)

            self.bs_quarterly_report_df = pd.concat(
                [balance_sheet.quarterly_reports, self.bs_quarterly_report_df],
                axis=1
            )

            self.bs_annual_report_df = pd.concat(
                [balance_sheet.annual_reports, self.bs_annual_report_df],
                axis=1
            )











