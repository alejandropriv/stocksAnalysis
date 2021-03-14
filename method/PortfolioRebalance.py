from utilities.Constants import Constants
from method.Method import Method
from utilities.Handlers import Handlers

import pandas as pd
import numpy as np


# Good for Bullish market
# Rebalance Every certain specific time: i.e. 3M
# Also works for short
class PortfolioRebalance(Method):
    def __init__(self, df=None):
        super().__init__()

    def back_test(self):

        """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""
        super().backtest()
        ################################ Backtesting ####################################
        PortfolioRebalance.pfolio()

    """Returns cumulative portfolio return
    DF = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""

    # function to calculate portfolio return iteratively
    @staticmethod
    def pfolio(df, m, x):

        in_d = Handlers.get_standard_input_data(df)
        tickers = in_d[Constants.get_tickers_key()]
        pricesk = in_d[Constants.get_prices_key()]
        df = in_d[Constants.get_input_df_key()]

        portfolio = []
        monthly_ret = [0]
        for i in range(len(df)):
            if len(portfolio) > 0:
                monthly_ret.append(df[portfolio].iloc[i, :].mean())
                bad_stocks = df[portfolio].iloc[i, :].sort_values(ascending=True)[:x].index.values.tolist()
                portfolio = [t for t in portfolio if t not in bad_stocks]
            fill = m - len(portfolio)
            new_picks = df.iloc[i, :].sort_values(ascending=False)[:fill].index.values.tolist()
            portfolio = portfolio + new_picks
            print(portfolio)
        monthly_ret_df = pd.DataFrame(np.array(monthly_ret), columns=["mon_ret"])
        return monthly_ret_df

        # calculating overall strategy's KPIs
        CAGR(pflio(return_df, 6, 3))
        sharpe(pflio(return_df, 6, 3), 0.025)
        max_dd(pflio(return_df, 6, 3))

        # calculating KPIs for Index buy and hold strategy over the same period
        DJI = yf.download("^DJI", dt.date.today() - dt.timedelta(3650), dt.date.today(), interval='1mo')
        DJI["mon_ret"] = DJI["Adj Close"].pct_change().fillna(0)
        CAGR(DJI)
        sharpe(DJI, 0.025)
        max_dd(DJI)

        # visualization
        fig, ax = plt.subplots()
        plt.plot((1 + pflio(return_df, 6, 3)).cumprod())
        plt.plot((1 + DJI["mon_ret"].reset_index(drop=True)).cumprod())
        plt.title("Index Return vs Strategy Return")
        plt.ylabel("cumulative return")
        plt.xlabel("months")
        ax.legend(["Strategy Return", "Index Return"])
        plt.show()
