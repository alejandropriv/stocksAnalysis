import unittest

import matplotlib.pyplot as plt


from strategy.StrategyManager import StrategyManager

from strategy.SMonthlyRebalance import SMonthlyRebalance
from strategy.test_strategies.StrategyXXII import StrategyXXII

from plotter.Plotter import Plotter

import datetime


DEVELOPMENT = True

class TestMethods(unittest.TestCase):

    def test_portfolio_rebalance(self):

        tickers = ["MMM","AXP","T","BA","CAT","CSCO","KO", "XOM","GE","GS","HD",
                   "IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV",
                   "UNH","VZ","V","WMT","DIS"]

        strategies = [SMonthlyRebalance()]

        smanager = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = smanager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                for kpi in stock.kpis:
                    print(kpi.df)

        if DEVELOPMENT == True:
            plt.show()



if __name__ == '__main__':
    unittest.main()
