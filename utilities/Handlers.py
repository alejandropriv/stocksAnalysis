import pandas as pd
from utilities.Constants import Constants


class Handlers:

    @staticmethod
    def get_standard_input_data(df):

        if df is None:
            raise ValueError("Error: Dataframe has not been provided, there is no data to calculate the requested KPI")

        input_data = {}

        # Set dataFrame keys
        adj_close_key = Constants.get_adj_close_key()
        close_key = Constants.get_close_key()

        if adj_close_key in df.columns is True:
            prices_key = adj_close_key

        else:
            prices_key = close_key

        prices_temp = pd.DataFrame()

        #TODO: Create a utilities class
        df.columns = pd.MultiIndex.from_tuples(df.columns.values)
        tickers = df.columns.levels[0]

        df_list = []
        for ticker in tickers:
            df_list.append(
                pd.concat(
                    [df[ticker].loc[:, [prices_key]], prices_temp],
                    axis=1,
                    keys=[ticker]
                )
            )

        input_df =\
            pd.concat(
                df_list,
                axis=1
            )

        input_data[Constants.get_prices_key()] = prices_key
        input_data[Constants.get_tickers_key()] = tickers
        input_data[Constants.get_input_df_key()] = input_df

        return input_data

