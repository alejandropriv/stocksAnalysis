from utilities.Constants import Constants as Ct
from indicators.Indicator import Indicator
import pandas as pd



class ATR(Indicator):

    # price is Dataframe
    def __init__(self, params=None):
        super().__init__(params)
        if not params:
            self.params = {}


    def calculate(self, df, params):
        """function to calculate True Range and Average True Range"""

        super().calculate(df, params)

        self.result = ATR.get_atr(df, self.params)
        return self.result


    @staticmethod
    def get_atr(input_df, params=None):

        n = params["n"]
        
        # Set temp dataframe keys
        h_l_key = Ct.get_key("H-L")
        h_pc_key = Ct.get_key("H-PC")
        l_pc_key = Ct.get_key("L-PC")
        tr_key = Ct.get_key("TR")

        df_data = input_df.copy()
        df_data.columns = df_data.columns.droplevel(1)


        df_data[h_l_key] = abs(df_data[Ct.high_key()] - df_data[Ct.low_key()])
        df_data[h_pc_key] = abs(df_data[Ct.high_key()] - df_data[self.prices_key].shift(1))
        df_data[l_pc_key] = abs(df_data[Ct.low_key()] - df_data[self.prices_key].shift(1))
        df_data[tr_key] = df_data[[h_l_key, h_pc_key, l_pc_key]].max(axis=1, skipna=False)
        df_data[Ct.atr_key()] = df_data[tr_key].rolling(n).mean()
        # df[Ct.atr_key()] = df[tr_key].ewm(span=n,adjust=False,min_periods=n).mean()
        # df_data.dropna(inplace=True, axis=0)

        df_data.drop([h_l_key, h_pc_key, l_pc_key], axis=1, inplace=True)

        df_result.append(df_data.loc[:, [Ct.atr_key(), tr_key]])

    self.df = pd.concat(df_result, axis=1, keys=self.tickers)


    return self.df



