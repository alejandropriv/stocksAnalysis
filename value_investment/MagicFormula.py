import pandas as pd
from value_investment.ValueInvestmentMetric import ValueInvestmentMetric


class MagicFormula(ValueInvestmentMetric):

    def __init__(self, fundamentals=None):
        super().__init__()

        if fundamentals is not None:
            self.set_input_data(fundamentals)

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

            df_list_data = [
                MagicFormula.add_level(ticker, fundamentals.overview_df),
                MagicFormula.add_level(ticker, fundamentals.balance_sheet_ar_df),
                MagicFormula.add_level(ticker, fundamentals.income_statement_ar_df),
                MagicFormula.add_level(ticker, fundamentals.cashflow_ar_df)]

            # TODO: Check if this works for bulk
            fundamentals_df = pd.DataFrame()

            for data in df_list_data:
                fundamentals_df = fundamentals_df.append(data)

            self.data_df = pd.concat([fundamentals_df, self.data_df], axis=1, join='outer')
            print("")


    @staticmethod
    def add_level(ticker, df):
        fundamentals_temp = pd.DataFrame()
        concat_df = None

        if ticker in df:
            # Concat latest available period
            concat_df = pd.concat(
                [df[ticker].iloc[:, [0]], fundamentals_temp],
                axis=1,
                keys=[ticker])

        return concat_df

    def calculate(self):


        self.data_df.sort_index(inplace=True)

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)

        print("data")
        print(self.data_df)

        print(self.data_df.index)

        net_income_key = "netIncomeApplicableToCommonShares"
        operating_cashflow_key = "operatingCashflow"
        total_current_assets_key = "totalCurrentAssets",
        total_current_liabilities_key = "totalCurrentLiabilities",
        ppe_key = "propertyPlantEquipment",
        preferred_stock = "preferredStockAndOtherAdjustments",
        minority_interest = "minorityIInterest",

        ebit_key = "ebit"
        total_debt_key = "TotalDebt"
        long_term_debt_key = "totalLongTermDebt"
        short_term_debt_key = "shortTermDebt"
        capital_lease_obligations_key = "capitalLeaseObligations"
        preferred_stock_total_equity_key = "preferredStockTotalEquity"
        total_current_assets_key = "totalCurrentAssets"
        total_current_liabilities_key = "totalCurrentLiabilities"
        cash_key = "cash"
        dividend_yield_key = "ForwardAnnualDividendYield"


        market_cap_key = "MarkedCapitalization"
        capex_key = "capitalExpenditures"
        book_value_key = "BookValue"
        property_plant_equipment = "propertyPlantEquipment"

        tev_key = "TEV"
        earning_yield_key = "EarningYield"
        book_to_market_key = "BookToMkt"
        return_on_capital = "ROC"





        transpose_df = self.data_df.transpose()

        # calculating relevant financial metrics for each stock
        final_stats_df = pd.DataFrame()
        final_stats_df[ebit_key] = transpose_df[ebit_key]
        final_stats_df[total_debt_key] = transpose_df[long_term_debt_key] +\
                                     transpose_df[short_term_debt_key] +\
                                     transpose_df[capital_lease_obligations_key]



        #todo: pick evto
        final_stats_df[tev_key] = transpose_df[market_cap_key].fillna(0) \
                                + transpose_df[total_debt_key].fillna(0) \
                                + transpose_df[preferred_stock_total_equity_key].fillna(0) \
                                + transpose_df["MinInterest"].fillna(0) \
                                - transpose_df[cash_key].fillna(0)
        final_stats_df[earning_yield_key] = final_stats_df[ebit_key] / final_stats_df[tev_key]
        #final_stats_df["FCFYield"] = (transpose_df["CashFlowOps"] - transpose_df[capex_key]) / transpose_df[market_cap_key]
        final_stats_df[return_on_capital] = transpose_df[ebit_key] / (transpose_df[property_plant_equipment] + transpose_df[total_current_assets_key] - transpose_df[total_current_liabilities_key])
        final_stats_df[book_to_market_key] = transpose_df[book_value_key] / transpose_df[market_cap_key]
        final_stats_df[dividend_yield_key] = transpose_df[dividend_yield_key]

        ################################Output Dataframes##############################

        # finding value stocks based on Magic Formula
        final_stats_val_df = final_stats_df.loc[tickers, :]
        final_stats_val_df["CombRank"] = final_stats_val_df["EarningYield"].rank(ascending=False, na_option='bottom') + \
                                         final_stats_val_df["ROC"].rank(ascending=False, na_option='bottom')
        final_stats_val_df["MagicFormulaRank"] = final_stats_val_df["CombRank"].rank(method='first')
        value_stocks = final_stats_val_df.sort_values("MagicFormulaRank").iloc[:, [2, 4, 8]]
        print("------------------------------------------------")
        print("Value stocks based on Greenblatt's Magic Formula")
        print(value_stocks)

        # finding highest dividend yield stocks
        high_dividend_stocks = final_stats_df.sort_values(dividend_yield, ascending=False).iloc[:, 6]
        print("------------------------------------------------")
        print("Highest dividend paying stocks")
        print(high_dividend_stocks)

        # # Magic Formula & Dividend yield combined
        final_stats_df["CombRank"] = final_stats_df["EarningYield"].rank(ascending=False, method='first') \
                                     + final_stats_df["ROC"].rank(ascending=False, method='first') \
                                     + final_stats_df[dividend_yield].rank(ascending=False, method='first')
        final_stats_df["CombinedRank"] = final_stats_df["CombRank"].rank(method='first')
        value_high_div_stocks = final_stats_df.sort_values("CombinedRank").iloc[:, [2, 4, 6, 8]]
        print("------------------------------------------------")
        print("Magic Formula and Dividend Yield combined")
        print(value_high_div_stocks)
