import unittest

import matplotlib.pyplot as plt

from strategy.StrategyManager import StrategyManager

from strategy.test_strategies.StrategyXX import StrategyXX

import pprint

DEVELOPMENT = True


class TestKPI(unittest.TestCase):

    def test_KPI_cagr(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

        reports = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers
            )

        cagr_tsla = reports['StrategyXX']['kpi']['TSLA']['CAGR']

        self.assertEqual(0.7093784038450781, cagr_tsla)


    def test_KPI_calmar(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

        reports = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers
            )

        calmar_tsla = reports['StrategyXX']['kpi']['TSLA']['Calmar']
        self.assertEqual(1.1700790532917946, calmar_tsla)



    def test_KPI_volatility(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

        reports = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers
            )


        volatility_tsla = reports['StrategyXX']['kpi']['TSLA']['Volatility']
        self.assertEqual(0.5809557173271221, volatility_tsla)



    def test_KPI_max_drawdown(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

        reports = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers
            )

        max_drawdown_tsla = reports['StrategyXX']['kpi']['TSLA']['MaxDrawdown']
        self.assertEqual(0.6062653645917145, max_drawdown_tsla)


    def test_KPI_sharpe(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

        reports = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers
            )

        sharpe_tsla = reports['StrategyXX']['kpi']['TSLA']['Sharpe']
        self.assertEqual(1.1962674316083073, sharpe_tsla)


    def test_KPI_sortino(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyXX()]

        reports = \
            StrategyManager.load_strategies(
                strategies=strategies,
                tickers=tickers
            )

        sortino_tsla = reports['StrategyXX']['kpi']['TSLA']['Sortino']
        self.assertEqual(2.071479016783677, sortino_tsla)




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
