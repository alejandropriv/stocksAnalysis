import unittest

import matplotlib.pyplot as plt

from strategy.StrategyManager import StrategyManager

from strategy.test_strategies.StrategyXX import StrategyXX
from strategy.test_strategies.StrategyXXII import StrategyXXII

from plotter.Plotter import Plotter

import datetime

DEVELOPMENT = True


class TestKPI(unittest.TestCase):

    def test_KPI(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

        results = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers
            )

        for key in results:
            for stock in results[key]:
                stock.print()

        if DEVELOPMENT == True:
            plt.show()


    @staticmethod
    def print_report(reports):
        for report in reports:
            report.print()

    def test_calmar(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXXI()]

        smanager = \
            StrategyManager(
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

    def test_max_drawdown(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXXII()]

        smanager = \
            StrategyManager(
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
