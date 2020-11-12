import pandas as pd
from value_investment.ValueInvestmentMetric import ValueInvestmentMetric


class MagicFormula(ValueInvestmentMetric):

    def __init__(self, fundamentals=None):
        super().__init__()

        if fundamentals is not None:
            self.set_input_data(fundamentals)

    def set_input_data(self, fundamentals):
        super().set_input_data(fundamentals)

        if fundamentals.balance_sheet_ar_df is None or \
                fundamentals.income_statement_ar_df is None or \
                fundamentals.cashflow_ar_df is None:

            raise ValueError("Not Enough information to calculate the Magic "
                             "Formula: BSAR:{}, ISAR:{}, CFAR:{}".
                             format(fundamentals.balance_sheet_ar_df,
                                    fundamentals.income_statement_ar_df,
                                    fundamentals.cashflow_ar_df))

        self.tickers = fundamentals.balance_sheet_ar_df.columns.levels[0]

        df_list_data = []


        for ticker in self.tickers:
            # df_list_overview.append(
            #    MagicFormula.add_level(ticker,
            #                           fundamentals.overview_df)
            # )
            df_list_data.append(
                MagicFormula.add_level(ticker,
                                       fundamentals.balance_sheet_ar_df)
            )
            df_list_data.append(
                MagicFormula.add_level(ticker,
                                       fundamentals.income_statement_ar_df)
            )

            df_list_data.append(
                MagicFormula.add_level(ticker,
                                       fundamentals.cashflow_ar_df)
            )

        self.data_df = pd.DataFrame()
        for data in df_list_data:
            self.data_df = self.data_df.append(data)



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

        print("data")
        print(self.data_df)
        self.data_df.sort_index(inplace=True)

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)

        print(self.data_df.index)
        print(self.data_df)

        required_data = ["ebit", "???marketcap??", "netIncome", "","", "totalCurrentAssets", "totalCurrentLiabilities", "propertyPlantEquipment", "", "totalLiabilities", "", "dividendPayout"]


