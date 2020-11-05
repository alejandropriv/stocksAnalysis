import pandas as pd
from value_investment.ValueInvestmentMetric import ValueInvestmentMetric


class MagicFormula(ValueInvestmentMetric):

    def __init__(self, fundamentals=None):
        super().__init__()
        self.fundamentals_df = None
        self.fields = pd.DataFrame()

        if fundamentals is not None:
            self.set_input_data(fundamentals)

    def set_input_data(self, fundamentals):
        super().set_input_data(fundamentals)

        fundamentals_temp = pd.DataFrame()

        for ticker in self.tickers:
            fundamentals_temp = self.concat_df(old_df=fundamentals_temp,
                                               df=fundamentals.balance_sheet_ar_df,
                                               ticker=ticker)

        self.fundamentals_df = fundamentals_temp.copy()


    @staticmethod
    def concat_df(old_df, df, ticker):

        df_concat = pd.concat(
            [df[ticker].loc[:, [0]], old_df],
            axis=1,
            keys=[ticker]
        )
        return df_concat

    def calculate(self):
        ebit_key = "ebit"
        self.fields[ebit_key] = self.fundamentals_df.income_statement_ar_df.loc["ebit"]
        self.fields["ebit"] = self.fundamentals_df.income_statement_ar_df["ebit"]
        self.fields["ebit"] = self.fundamentals_df.income_statement_ar_df["ebit"]
        self.fields["ebit"] = self.fundamentals_df.income_statement_ar_df["ebit"]
        self.fields["ebit"] = self.fundamentals_df.income_statement_ar_df["ebit"]
        self.fields["ebit"] = self.fundamentals_df.income_statement_ar_df["ebit"]
        self.fields["ebit"] = self.fundamentals_df.income_statement_ar_df["ebit"]
        self.fields["ebit"] = self.fundamentals_df.income_statement_ar_df["ebit"]
        self.fields["ebit"] = self.fundamentals_df.income_statement_ar_df["ebit"]

        print("BalanceSheet")
        print(self.fundamentals_df.balance_sheet_ar_df)
        print("IncomeStatement")
        print(self.fundamentals_df.income_statement_ar_df)
        print("CashFlow")
        print(self.fundamentals_df.cashflow_ar_df)
        print("Overview")
        print(self.fundamentals_df.overview_df)
