from fundamentals.BalanceSheet import BalanceSheet
from fundamentals.CashFlow import CashFlow
from fundamentals.Statistics import Statistics
from fundamentals.IncomeStatement import IncomeStatement


class PiotroskyFScore:

    def __init__(self, ticker):
        self.ticker = ticker

        self.income_statement = IncomeStatement(self.ticker)

        self.balance_sheet = BalanceSheet(self.ticker)

        self.cash_flow = CashFlow(self.ticker)

        self.statistics = Statistics(self.ticker)

        self.income_statement.get_data()

        # storing information in pandas dataframe
        combined_financials_cy = pd.DataFrame(financial_dir_cy)
        combined_financials_cy.dropna(axis=1, inplace=True)  # dropping columns with all NaN values
        combined_financials_py = pd.DataFrame(financial_dir_py)
        combined_financials_py.dropna(axis=1, inplace=True)
        combined_financials_py2 = pd.DataFrame(financial_dir_py2)
        combined_financials_py2.dropna(axis=1, inplace=True)
        tickers = combined_financials_cy.columns  # updating the tickers list based on only those tickers whose values were successfully extracted

        # selecting relevant financial information for each stock using fundamental data
        self.stats = ["Net income applicable to common shares",
                      "Total assets",
                      "Total cash flow from operating activities",
                      "Long-term debt",
                      "Other liabilities",
                      "Total current assets",
                      "Total current liabilities",
                      "Common stock",
                      "Total revenue",
                      "Gross profit"]  # change as required

        self.indx = ["NetIncome",
                     "TotAssets",
                     "CashFlowOps",
                     "LTDebt",
                     "OtherLTDebt",
                     "CurrAssets",
                     "CurrLiab",
                     "CommStock",
                     "TotRevenue",
                     "GrossProfit"]

        self.df_cy
        self.df_py
        self.df_py2


    def calculate(self):
        """function to calculate f score of each stock and output information as dataframe"""
        f_score = {}
        tickers = df_cy.columns
        for ticker in tickers:
            ROA_FS = int(df_cy.loc["NetIncome", ticker] / (
                    (df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2) > 0)
            CFO_FS = int(df_cy.loc["CashFlowOps", ticker] > 0)
            ROA_D_FS = int(df_cy.loc["NetIncome", ticker] / (
                    df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2 > df_py.loc[
                                   "NetIncome", ticker] / (
                                    df_py.loc["TotAssets", ticker] + df_py2.loc["TotAssets", ticker]) / 2)
            CFO_ROA_FS = int(df_cy.loc["CashFlowOps", ticker] / df_cy.loc["TotAssets", ticker] > df_cy.loc[
                "NetIncome", ticker] / ((df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2))
            LTD_FS = int((df_cy.loc["LTDebt", ticker] + df_cy.loc["OtherLTDebt", ticker]) < (
                    df_py.loc["LTDebt", ticker] + df_py.loc["OtherLTDebt", ticker]))
            CR_FS = int((df_cy.loc["CurrAssets", ticker] / df_cy.loc["CurrLiab", ticker]) > (
                    df_py.loc["CurrAssets", ticker] / df_py.loc["CurrLiab", ticker]))
            DILUTION_FS = int(df_cy.loc["CommStock", ticker] <= df_py.loc["CommStock", ticker])
            GM_FS = int((df_cy.loc["GrossProfit", ticker] / df_cy.loc["TotRevenue", ticker]) > (
                    df_py.loc["GrossProfit", ticker] / df_py.loc["TotRevenue", ticker]))
            ATO_FS = int(df_cy.loc["TotRevenue", ticker] / (
                    (df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2) > df_py.loc[
                                "TotRevenue", ticker] / (
                                (df_py.loc["TotAssets", ticker] + df_py2.loc["TotAssets", ticker]) / 2))
            f_score[ticker] = [ROA_FS, CFO_FS, ROA_D_FS, CFO_ROA_FS, LTD_FS, CR_FS, DILUTION_FS, GM_FS, ATO_FS]
            f_score_df = pd.DataFrame(f_score,
                                      index=["PosROA", "PosCFO", "ROAChange", "Accruals", "Leverage", "Liquidity",
                                             "Dilution", "GM", "ATO"])
            return f_score_df
