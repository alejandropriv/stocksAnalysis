import unittest

import matplotlib.pyplot as plt


from strategy.StrategyManager import StrategyManager

from strategy.test_strategies.StrategyXX import StrategyXX

from plotter.Plotter import Plotter

import datetime


DEVELOPMENT = True

class TestKPI(unittest.TestCase):

    def test_CAGR(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

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


        #
        # test_date = "14/07/2020"
        # test_df = stocks_per_strategy[StrategyIII.name][0].price_info
        # ticker = "TSLA"
        # values = [318.0, 286.2, 311.2, 303.359, 117090500.0]
        #
        # i = 0
        # for metric in ["High", "Low", "Open", "Close", "Volume"]:
        #     value = TestIndicators.truncate(
        #         test_df[ticker][metric].loc[
        #             test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
        #             ].iloc[0])
        #     assert value == TestIndicators.truncate(values[i]), value
        #     i += 1
        #
        #
        # print("Analysis has been run")




if __name__ == '__main__':
    unittest.main()
