import pandas as pd
from value_investment.ValueInvestmentMetric import ValueInvestmentMetric


class MagicFormula(ValueInvestmentMetric):

    def __init__(self, fundamentals=None):
        super().__init__()
        self.fields = pd.DataFrame()

        if fundamentals is not None:
            self.set_input_data(fundamentals)

    def set_input_data(self, fundamentals):
        super().set_input_data(fundamentals)

        df_list_overview = []
        df_list_cashflow = []
        df_list_income_statement= []
        df_list_balance_sheet = []

        for ticker in self.tickers:
            # TODO: Continue fixing here
            df_list_overview.append(
                MagicFormula.add_level(ticker,
                                       fundamentals.overview_df)
            )
            df_list_income_statement.append(
                MagicFormula.add_level(ticker,
                                       fundamentals.income_statement_ar_df)
            )
            df_list_balance_sheet.append(
                MagicFormula.add_level(ticker,
                                       fundamentals.balance_sheet_ar_df)
            )
            df_list_cashflow.append(
                MagicFormula.add_level(ticker,
                                       fundamentals.cashflow_ar_df)
            )


        df_overview = pd.concat(
            df_list_overview,
            axis=1
        )
        df_balance_sheet = pd.concat(
            df_list_balance_sheet,
            axis=1
        )
        df_income_statement = pd.concat(
            df_list_income_statement,
            axis=1
        )
        df_cashflow = pd.concat(
            df_list_cashflow,
            axis=1
        )

        #TODO: Verify if copy is rebundant
        self.overview = df_overview
        self.balance_sheet = df_balance_sheet
        self.income_statement = df_income_statement
        self.cashflow = df_cashflow   # .copy()

        self.get_tickers()


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

        print("BalanceSheet")
        print(self.balance_sheet)
        print("IncomeStatement")
        print(self.income_statement)
        print("CashFlow")
        print(self.cashflow)
        print("Overview")
        print(self.overview)



        ebit_key = "ebit"
        self.fields[ebit_key] = self.income_statement.loc[ebit_key]
        print(self.fields)

