import unittest

import matplotlib.pyplot as plt

from strategy.StrategyManager import StrategyManager

from strategy.test_strategies.StrategyXX import StrategyXX

import pprint

DEVELOPMENT = True


class TestKPI(unittest.TestCase):

    def test_KPI(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

        reports = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers
            )

        cagr_tsla = reports['StrategyXX']['kpi']['TSLA']['CAGR']
        calmar_tsla = reports['StrategyXX']['kpi']['TSLA']['Calmar']
        volatility_tsla = reports['StrategyXX']['kpi']['TSLA']['Volatility']
        sharpe_tsla = reports['StrategyXX']['kpi']['TSLA']['Sharpe']
        sortino_tsla = reports['StrategyXX']['kpi']['TSLA']['Sortino']
        max_drawdown_tsla = reports['StrategyXX']['kpi']['TSLA']['MaxDrawdown']

        self.assertEqual(cagr_tsla, 0.7093784038450781)
        self.assertEqual(calmar_tsla, 1.1700790532917946)
        self.assertEqual(max_drawdown_tsla, 0.6062653645917145)
        self.assertEqual(volatility_tsla, 0.5809557173271221)
        self.assertEqual(sharpe_tsla, 1.1962674316083073)
        self.assertEqual(sortino_tsla, 2.071479016783677)


        print(reports)

        if DEVELOPMENT == True:
            plt.show()


    def test_KPI_bulk(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

        reports = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )


        if DEVELOPMENT == True:
            plt.show()



    @staticmethod
    def print_report(reports):
        for report in reports:
            report.print()



if __name__ == '__main__':
    unittest.main()
