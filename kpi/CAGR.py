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
        "function to calculate the Cumulative Annual Growth Rate of a trading strategy"

        self.df["daily_ret"] = self.df["Adj Close"].pct_change()
        self.df["cum_return"] = (1 + self.df["daily_ret"]).cumprod()
        n = len(self.df) / 252
        self.value = (self.df["cum_return"][-1]) ** (1 / n) - 1
        return self.value

