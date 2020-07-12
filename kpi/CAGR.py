from utilities.Constants import Constants
from kpi.KPI import KPI



class CAGR(KPI):
    def __init__(self, df):
        super().__init__()

        self.adj_close_key = None

        if df is not None:
            self.set_input_data(df)


    def set_input_data(self, df):
        super().set_input_data(df)
        self.adj_close_key = Constants.get_adj_close_key(self.ticker)

        self.df = df.iloc[:, [self.adj_close_key]].copy()






    def calculate(self):
        """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""
        super().calculate()

        daily_ret_key = Constants.get_daiy_ret_key(self.ticker)
        cum_ret_key = Constants.get_key(self.ticker, "cum_return")

        self.df[daily_ret_key] = self.df[self.adj_close_key].pct_change()
        self.df[cum_ret_key] = (1 + self.df[daily_ret_key]).cumprod()
        n = len(self.df) / 252
        self.value = (self.df[cum_ret_key][-1]) ** (1 / n) - 1
        return self.value

