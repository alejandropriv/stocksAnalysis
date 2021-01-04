import pandas as pd
from value_investment.ValueInvestmentMetric import ValueInvestmentMetric


class PiotroskyFScore(ValueInvestmentMetric):


    def __init__(self, fundamentals=None):
        super().__init__()

        if fundamentals is not None:
            self.set_input_data(fundamentals)


    @staticmethod
    def add_level(ticker, df):

        # TODO: Raise exception if the process can not be done, and design exception handling process
        fundamentals_temp = pd.DataFrame()
        concat_df = [None]

        if ticker in df:
            # Concat latest available period
            concat_df.append(pd.concat(
                [df[ticker].iloc[:, [0]], fundamentals_temp],
                axis=1,
                keys=[ticker]))

            concat_df.append(pd.concat(
                [df[ticker].iloc[:, [1]], fundamentals_temp],
                axis=1,
                keys=[ticker]))

            concat_df.append(pd.concat(
                [df[ticker].iloc[:, [2]], fundamentals_temp],
                axis=1,
                keys=[ticker]))

        return concat_df


    def set_input_data(self, fundamentals):
        super().set_input_data(fundamentals)

        if fundamentals.overview_df is None or \
                fundamentals.balance_sheet_ar_df is None or \
                fundamentals.income_statement_ar_df is None or \
                fundamentals.cashflow_ar_df is None:
            raise ValueError("Not Enough information to calculate the Magic "
                             "Formula: BSAR:{}, ISAR:{}, CFAR:{}".
                             format(fundamentals.balance_sheet_ar_df,
                                    fundamentals.income_statement_ar_df,
                                    fundamentals.cashflow_ar_df))

        self.tickers = fundamentals.balance_sheet_ar_df.columns.levels[0]

        self.data_df = pd.DataFrame()

        for ticker in self.tickers:

            fundamentals.overview_df.rename(columns={"data": fundamentals.balance_sheet_ar_df[ticker].columns[0]},
                                            inplace=True)

            PiotroskyFScore.add_level(ticker, fundamentals.overview_df) # TODO: WTF
            bs_3y = PiotroskyFScore.add_level(ticker, fundamentals.balance_sheet_ar_df)
            is_3y = PiotroskyFScore.add_level(ticker, fundamentals.income_statement_ar_df)
            cf_3y = PiotroskyFScore.add_level(ticker, fundamentals.cashflow_ar_df)

            # TODO: Check if this works for bulk
            fundamentals_df = pd.DataFrame()

            for data in df_list_data:
                fundamentals_df = fundamentals_df.append(data)

            self.data_df = pd.concat([fundamentals_df, self.data_df], axis=1, join='outer')
            print("")



    def calculate(self):
        """function to calculate f score of each stock and output information as dataframe"""
        f_score = {}
        tickers = df_cy.columns
        for ticker in tickers:
            ROA_FS = int(df_cy.loc["NetIncome", ticker] / (
                        (df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2) > 0)
            CFO_FS = int(df_cy.loc["CashFlowOps", ticker] > 0)
            ROA_D_FS = int(
                df_cy.loc["NetIncome", ticker] / (df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2 >
                df_py.loc["NetIncome", ticker] / (df_py.loc["TotAssets", ticker] + df_py2.loc["TotAssets", ticker]) / 2)
            CFO_ROA_FS = int(
                df_cy.loc["CashFlowOps", ticker] / df_cy.loc["TotAssets", ticker] > df_cy.loc["NetIncome", ticker] / (
                            (df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2))
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
        f_score_df = pd.DataFrame(f_score, index=["PosROA", "PosCFO", "ROAChange", "Accruals", "Leverage", "Liquidity",
                                                  "Dilution", "GM", "ATO"])
        return f_score_df

