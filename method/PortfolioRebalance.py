# =============================================================================
# Backtesting strategy - I : Monthly portfolio rebalancing
# Author : Mayank Rasu (http://rasuquant.com/wp/)

# Please report bug/issues in the Q&A section
# =============================================================================

import numpy as np
import pandas as pd
from utilities.Constants import Constants as Ct
import matplotlib.pyplot as plt
from method.Method import Method
from data_analysis.Financials import Financials
from kpi.CAGR import CAGR
from kpi.Sharpe import Sharpe
from kpi.MaxDrawdown import MaxDrawdown


class PortfolioRebalance(Method):

    def __init__(self, stocks=None):
        super().__init__()


    # cagr = CAGR.get_cagr(pflio(return_df, 6, 3))
    def backtest(self, prices, ref_prices, params):

        m = params["m"]
        x = params["x"]
        interval = params[Ct.interval_key()]

        mon_ret_df = Financials.pct_change(prices)
        p_return = PortfolioRebalance.calculate(mon_ret_df, m, x)

        cagr_params = {Ct.interval_key(): interval}
        cagr = CAGR.get_cagr(p_return, cagr_params)
        sharpe_params = {"rf": 0.025, Ct.interval_key():interval}
        sharpe = Sharpe.get_sharpe(p_return, sharpe_params)
        max_dd = MaxDrawdown.get_max_drawdown(p_return)

        # calculating overall strategy's KPIs

        mon_ret_df = Financials.pct_change(ref_prices)
        p_return_ref = PortfolioRebalance.calculate(mon_ret_df, m, x)

        cagr_ref = CAGR.get_cagr(p_return, cagr_params)
        sharpe_params = {"rf": 0.025, Ct.interval_key():interval}
        sharpe_ref = Sharpe.get_sharpe(p_return_ref, sharpe_params)
        max_dd_ref = MaxDrawdown.get_max_drawdown(p_return_ref)

        print("CAGR - Portfolio: {}".format(cagr))
        print("Sharpe - Portfolio: {}".format(sharpe))
        print("MAX-Drawdown - Portfolio: {}".format(cagr))
        print("CAGR - Portfolio: {}".format(cagr_ref))
        print("Sharpe - Portfolio: {}".format(sharpe_ref))
        print("MAX-Drawdown - Ref: {}".format(max_dd_ref))

        PortfolioRebalance.plot(p_return, p_return_ref)



    # function to calculate portfolio return iteratively
    @staticmethod
    def calculate(input_df, m, x):
        """Returns cumulative portfolio return
        DF = dataframe with monthly return info for all stocks
        m = number of stock in the portfolio
        x = number of underperforming stocks to be removed from portfolio monthly"""
        df = input_df.copy()
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

        monthly_ret_df.columns = pd.MultiIndex.from_product([monthly_ret_df.columns, ['Portfolio']])
        return monthly_ret_df

    @staticmethod
    def plot(portfolio, reference):
        # visualization
        fig, ax = plt.subplots()
        plt.plot((1 + portfolio).cumprod())
        plt.plot((1 + reference.reset_index(drop=True)).cumprod())
        plt.title("Index Return vs Strategy Return")
        plt.ylabel("cumulative return")
        plt.xlabel("months")
        ax.legend(["Strategy Return", "Index Return"])
        plt.show()


