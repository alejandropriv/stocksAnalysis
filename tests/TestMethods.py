import unittest

from data.DataSource import DATASOURCETYPE

import matplotlib.pyplot as plt

from utilities.Constants import Constants as Ct

import datetime as dt

from stocks_model.StocksFactory import StocksFactory

from method.PortfolioRebalance import PortfolioRebalance

from plotter.Plotter import Plotter


DEVELOPMENT = True


class TestMethods(unittest.TestCase):

    def test_portfolio_rebalance(self):

        #  DJI constituent stocks
        tickers = ["MMM", "AXP", "T", "BA", "CAT", "CSCO", "KO", "XOM", "GE",
                   "GS", "HD", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT",
                   "NKE", "PFE", "PG", "TRV", "UNH", "VZ", "V", "WMT", "DIS"]

        ref_tickers = ["^DJI"]

        end_date = dt.datetime.now()  # dt.datetime(2021, 3, 7)
        interval = Ct.INTERVAL.MONTH

        conf = {
            Ct.tickers_key(): tickers,
            Ct.historical_type_key(): DATASOURCETYPE.YFINANCE,
            Ct.fundamentals_type_key(): None,
            Ct.fundamentals_options_key(): [],
            Ct.force_fundamentals_key(): False,
            Ct.indicators_key(): [],
            Ct.start_date_key(): end_date-dt.timedelta(3650),
            Ct.end_date_key(): end_date,
            Ct.interval_key(): interval,
            Ct.period_key(): None,
            Ct.bulk_key(): True
        }

        stocks = \
            StocksFactory.create_stocks(
                conf=conf
            )

        conf[Ct.tickers_key()] = ref_tickers

        stocks_ref = \
            StocksFactory.create_stocks(
                conf=conf
            )

        prices_df = stocks[0].get_prices_data(keys={Ct.adj_close_key(): True})
        ref_prices_df = stocks_ref[0].get_prices_data(keys={Ct.adj_close_key(): True})

        pr = PortfolioRebalance()
        params = {"m": 6, "x": 3, Ct.interval_key(): conf[Ct.interval_key()]}
        pr.backtest(prices_df, ref_prices_df, params)

        #self.assertEqual(0.7093784038450781, result['TSLA'][Ct.cagr_key()][0])


    def test_portfolio_rebalance2(self):

        tickers = ["MMM", "AXP", "T", "BA", "CAT", "CSCO", "KO", "XOM", "GE", "GS", "HD",
                   "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV",
                   "UNH", "VZ", "V", "WMT", "DIS"]

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
