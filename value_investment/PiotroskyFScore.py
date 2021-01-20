import pandas as pd
from value_investment.ValueInvestmentMetric import ValueInvestmentMetric


class PiotroskyFScore(ValueInvestmentMetric):


    def __init__(self, fundamentals=None):
        super().__init__()

        if fundamentals is not None:
            self.set_input_data(fundamentals)

        self.cy_data = pd.DataFrame()
        self.py_data = pd.DataFrame()
        self.p2y_data = pd.DataFrame()

    @staticmethod
    def add_level(ticker, df):
        fundamentals_temp = pd.DataFrame()
        concat_df = None

        if ticker in df:
            # Concat latest available period
            concat_df = pd.concat(
                [df[ticker].iloc[:, [0,1,2]], fundamentals_temp], # TODO change [0,1,2] to a nicer one
                axis=1,
                keys=[ticker])

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

            # PiotroskyFScore.add_level(ticker, fundamentals.overview_df) # TODO: WTF
            bs_3y = PiotroskyFScore.add_level(ticker, fundamentals.balance_sheet_ar_df)
            is_3y = PiotroskyFScore.add_level(ticker, fundamentals.income_statement_ar_df)
            cf_3y = PiotroskyFScore.add_level(ticker, fundamentals.cashflow_ar_df)

            df_list_data = [
                bs_3y,
                is_3y,
                cf_3y
            ]

            fundamentals_df = pd.DataFrame()
            cy_df = pd.DataFrame()
            py_df = pd.DataFrame()
            p2y_df = pd.DataFrame()


            for data in df_list_data:
                fundamentals_df = fundamentals_df.append(data)
                cy_df = self.cy_data.append(data.iloc[:, [0]])
                py_df = self.py_data.append(data.iloc[:, [1]])
                p2y_df = self.p2y_data.append(data.iloc[:, [2]])

            self.cy_data = pd.concat([cy_df, self.cy_data], axis=1, join='outer')
            self.py_data = pd.concat([py_df, self.py_data], axis=1, join='outer')
            self.p2y_data = pd.concat([p2y_df, self.cy_data], axis=1, join='outer')
            print("")



    def calculate(self):

        self.data_df.sort_index(inplace=True)

        print("----------------- data -------------------")
        print(self.data_df)

        print(self.data_df.index)

        net_income_cf_key = "netIncome"
        total_assets_bs_key = "totalAssets"
        cash_flow_ops_cf_key = "operatingCashflow"
        long_term_debt_bs_key = "longTermDebt"
        other_long_term_debt_bs_key = "OtherLTDebt"#
        current_assets_bs_key = "CurrAssets"
        current_liabilities_bs_key = "CurrLiab"
        common_stock_bs_key = "CommStock"
        gross_profit_bs_key = "GrossProfit"
        total_revenue_bs_key = "TotRevenue"




        for ticker in self.data_df.columns.get_level_values(0):
            self.data_df[ticker] = pd.to_numeric(self.data_df[ticker][self.data_df[ticker].columns[0]].values,
                                                 errors='coerce')


        """function to calculate f score of each stock and output information as dataframe"""
        f_score = {}
        tickers = self.cy_data.columns
        for ticker in tickers:
            ROA_FS = int(self.cy_data.loc[net_income_cf_key, ticker] / (
                        (self.cy_data.loc[total_assets_bs_key, ticker] + self.py_data.loc[total_assets_bs_key, ticker]) / 2) > 0)
            CFO_FS = int(self.cy_data.loc[cash_flow_ops_cf_key, ticker] > 0)
            ROA_D_FS = int(
                self.cy_data.loc[net_income_cf_key, ticker] / (self.cy_data.loc[total_assets_bs_key, ticker] + self.py_data.loc[total_assets_bs_key, ticker]) / 2 >
                self.py_data.loc[net_income_cf_key, ticker] / (self.py_data.loc[total_assets_bs_key, ticker] + self.p2y_data.loc[total_assets_bs_key, ticker]) / 2)
            CFO_ROA_FS = int(
                self.cy_data.loc[cash_flow_ops_cf_key, ticker] / self.cy_data.loc[total_assets_bs_key, ticker] > self.cy_data.loc[net_income_cf_key, ticker] / (
                            (self.cy_data.loc[total_assets_bs_key, ticker] + self.py_data.loc[total_assets_bs_key, ticker]) / 2))
            LTD_FS = int((self.cy_data.loc[long_term_debt_bs_key, ticker] + self.cy_data.loc[other_long_term_debt_bs_key, ticker]) < (
                        self.py_data.loc[long_term_debt_bs_key, ticker] + self.py_data.loc[other_long_term_debt_bs_key, ticker]))
            CR_FS = int((self.cy_data.loc[current_assets_bs_key, ticker] / self.cy_data.loc[current_liabilities_bs_key, ticker]) > (
                        self.py_data.loc[current_assets_bs_key, ticker] / self.py_data.loc[current_liabilities_bs_key, ticker]))
            DILUTION_FS = int(self.cy_data.loc[common_stock_bs_key, ticker] <= self.py_data.loc[common_stock_bs_key, ticker])
            GM_FS = int((self.cy_data.loc[gross_profit_bs_key, ticker] / self.cy_data.loc[total_revenue_bs_key, ticker]) > (
                        self.py_data.loc[gross_profit_bs_key, ticker] / self.py_data.loc[total_revenue_bs_key, ticker]))
            ATO_FS = int(self.cy_data.loc[total_revenue_bs_key, ticker] / (
                        (self.cy_data.loc[total_assets_bs_key, ticker] + self.py_data.loc[total_assets_bs_key, ticker]) / 2) > self.py_data.loc[
                             total_revenue_bs_key, ticker] / (
                                     (self.py_data.loc[total_assets_bs_key, ticker] + self.p2y_data.loc[total_assets_bs_key, ticker]) / 2))
            f_score[ticker] = [ROA_FS, CFO_FS, ROA_D_FS, CFO_ROA_FS, LTD_FS, CR_FS, DILUTION_FS, GM_FS, ATO_FS]
        f_score_df = pd.DataFrame(f_score, index=["PosROA", "PosCFO", "ROAChange", "Accruals", "Leverage", "Liquidity",
                                                  "Dilution", "GM", "ATO"])
        return f_score_df

