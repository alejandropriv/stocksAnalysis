import pandas as pd
from value_investment.ValueInvestmentMetric import ValueInvestmentMetric


# TODO Check the stocks were created with bulk=True and all the stocks are in only one datagram

class MagicFormula(ValueInvestmentMetric):

    def __init__(self, fundamentals=None):
        super().__init__()

        if fundamentals is not None:
            self.set_input_data(fundamentals)


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

            fundamentals_df = pd.DataFrame()

            for data in df_list_data:
                fundamentals_df = fundamentals_df.append(data)

            self.data_df = pd.concat([fundamentals_df, self.data_df], axis=1, join='outer')
            print("")


    def calculate(self):

        self.data_df.sort_index(inplace=True)

        print("----------------- data -------------------")
        print(self.data_df)

        print(self.data_df.index)

        operating_cashflow_key = "operatingCashflow"

        ebit_is_key = "ebit"

        long_term_debt_bs_key = "totalLongTermDebt"
        short_term_debt_bs_key = "shortTermDebt"
        capital_lease_obligations_bs_key = "capitalLeaseObligations"

        preferred_stock_bs_key = "preferredStockTotalEquity"
        minority_interest_is_key = "minorityInterest"
        cash_bs_key = "cash"

        property_plant_equipment_bs_key = "propertyPlantEquipment"
        total_current_assets_bs_key = "totalCurrentAssets"
        total_current_liabilities_bs_key = "totalCurrentLiabilities"

        dividend_yield_key = "ForwardAnnualDividendYield"

        capex_key = "capitalExpenditures"

        total_debt_key = "TotalDebt"
        earning_yield_key = "EarningYield"
        tev_key = "TEV"
        market_cap_ov_key = "MarketCapitalization"
        return_on_capital_key = "ROC"

        # TODO: Why are those even calculated
        book_to_market_key = "BookToMkt"
        book_value_key = "BookValue"


        fcf_yield_r_key = "FCFYield"
        comb_rank_r_key = "CombRank"
        magic_formula_rank_r_key = "MagicFormulaRank"
        combined_rank_r_key = "CombinedRank"


        for ticker in self.data_df.columns.get_level_values(0):
            self.data_df[ticker] = pd.to_numeric(self.data_df[ticker][self.data_df[ticker].columns[0]].values,
                                                 errors='coerce')

        num_tr_df = self.data_df.transpose()

        # calculating relevant financial metrics for each stock
        final_stats_df = pd.DataFrame()
        final_stats_df[ebit_is_key] = num_tr_df[ebit_is_key]
        final_stats_df[total_debt_key] = num_tr_df[long_term_debt_bs_key].fillna(0) + \
                                         num_tr_df[short_term_debt_bs_key].fillna(0) + \
                                         num_tr_df[capital_lease_obligations_bs_key].fillna(0)

        final_stats_df[tev_key] = final_stats_df[total_debt_key].fillna(0) \
                                + num_tr_df[market_cap_ov_key].fillna(0) \
                                + num_tr_df[preferred_stock_bs_key].fillna(0) \
                                + num_tr_df[minority_interest_is_key].fillna(0) \
                                - num_tr_df[cash_bs_key].fillna(0)
        # - (transpose_df[total_current_assets_bs_key].fillna(0) - transpose_df[total_current_liabilities_bs_key].fillna(0)) # CASH Approximation

        final_stats_df[earning_yield_key] = final_stats_df[ebit_is_key] / final_stats_df[tev_key]
        # TODO: Check what this metric really means
        final_stats_df[fcf_yield_r_key] = (num_tr_df[operating_cashflow_key] - num_tr_df[capex_key]) / num_tr_df[
            market_cap_ov_key]
        final_stats_df[return_on_capital_key] = num_tr_df[ebit_is_key] / (
                num_tr_df[property_plant_equipment_bs_key] + num_tr_df[total_current_assets_bs_key] - num_tr_df[
            total_current_liabilities_bs_key])
        final_stats_df[book_to_market_key] = num_tr_df[book_value_key] / num_tr_df[market_cap_ov_key]
        final_stats_df[dividend_yield_key] = num_tr_df[dividend_yield_key]

        # ###############################Output Dataframes##############################

        # finding value stocks based on Magic Formula
        final_stats_val_df = final_stats_df  # .loc[tickers, :]
        final_stats_val_df[comb_rank_r_key] = final_stats_val_df[earning_yield_key].rank(ascending=False,
                                                                                       na_option='bottom') + \
                                            final_stats_val_df[return_on_capital_key].rank(ascending=False,
                                                                                           na_option='bottom')
        final_stats_val_df[magic_formula_rank_r_key] = final_stats_val_df[comb_rank_r_key].rank(method='first')
        value_stocks = final_stats_val_df.sort_values(magic_formula_rank_r_key).iloc[:, [2, 4, 8]]
        print("------------------------------------------------")
        print("Value stocks based on Greenblatt's Magic Formula")
        print(value_stocks)

        # finding highest dividend yield stocks
        high_dividend_stocks = final_stats_df.sort_values(dividend_yield_key, ascending=False).iloc[:, 6]
        print("------------------------------------------------")
        print("Highest dividend paying stocks")
        print(high_dividend_stocks)

        # # Magic Formula & Dividend yield combined
        final_stats_df[comb_rank_r_key] = final_stats_df[earning_yield_key].rank(ascending=False, method='first') \
                                        + final_stats_df[return_on_capital_key].rank(ascending=False, method='first') \
                                        + final_stats_df[dividend_yield_key].rank(ascending=False, method='first')
        final_stats_df[combined_rank_r_key] = final_stats_df[comb_rank_r_key].rank(method='first')
        value_high_div_stocks = final_stats_df.sort_values(combined_rank_r_key).iloc[:, [2, 4, 6, 8]]
        print("------------------------------------------------")
        print("Magic Formula and Dividend Yield combined")
        print(value_high_div_stocks)
