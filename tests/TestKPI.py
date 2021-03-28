import unittest

from data.DataSource import DATASOURCETYPE
from stocks_model.StocksFactory import StocksFactory

from utilities.Constants import Constants as Ct

from kpi.CAGR import CAGR
from kpi.Calmar import Calmar
from kpi.MaxDrawdown import MaxDrawdown
from kpi.Volatility import Volatility
from kpi.Sharpe import Sharpe
from kpi.Sortino import Sortino


from data_analysis.Financials import Financials
import datetime as dt



DEVELOPMENT = True


class TestKPI(unittest.TestCase):

    def test_KPI_cagr(self):
        tickers = ["TSLA", "SPY"]
        interval = Ct.INTERVAL.DAY

        conf = {
            Ct.tickers_key(): tickers,
            Ct.historical_type_key(): DATASOURCETYPE.YFINANCE,
            Ct.fundamentals_type_key(): None,
            Ct.fundamentals_options_key(): [],
            Ct.force_fundamentals_key(): False,
            Ct.indicators_key(): [],
            Ct.start_date_key(): dt.datetime(2021, 3, 7)-dt.timedelta(1825),
            Ct.end_date_key(): dt.datetime(2021, 3, 7),
            Ct.interval_key(): interval,
            Ct.period_key(): None,
            Ct.bulk_key(): True

        }

        stocks = \
            StocksFactory.create_stocks(
                conf=conf
            )

        prices_df = stocks[0].get_prices_data(keys={Ct.adj_close_key(): True})

        df = Financials.pct_change(prices_df)

        params = {Ct.interval_key(): interval}
        cagr = CAGR()
        result = cagr.calculate(df, params)

        self.assertEqual(0.7093784038450781, result[Ct.cagr_key()]['TSLA'])
        self.assertEqual(0.1608091728848835, result[Ct.cagr_key()]['SPY'])



    def test_KPI_max_drawdown(self):
        tickers = ["TSLA", "SPY"]
        interval = Ct.INTERVAL.DAY

        conf = {
            Ct.tickers_key(): tickers,
            Ct.historical_type_key(): DATASOURCETYPE.YFINANCE,
            Ct.fundamentals_type_key(): None,
            Ct.fundamentals_options_key(): [],
            Ct.force_fundamentals_key(): False,
            Ct.indicators_key(): [],
            Ct.start_date_key(): dt.datetime(2021, 3, 7) - dt.timedelta(1825),
            Ct.end_date_key(): dt.datetime(2021, 3, 7),
            Ct.interval_key(): interval,
            Ct.period_key(): None,
            Ct.bulk_key(): True

        }

        stocks = \
            StocksFactory.create_stocks(
                conf=conf
            )

        prices_df = stocks[0].get_prices_data(keys={Ct.adj_close_key(): True})

        df = Financials.pct_change(prices_df)

        md = MaxDrawdown()
        result = md.calculate(df)

        self.assertEqual(0.6062653645917145, result[Ct.max_drawdown_key()]['TSLA'])
        self.assertEqual(0.3371725544013077, result[Ct.max_drawdown_key()]['SPY'])


    def test_KPI_calmar(self):
        tickers = ["TSLA", "SPY"]
        interval = Ct.INTERVAL.DAY

        conf = {
            Ct.tickers_key(): tickers,
            Ct.historical_type_key(): DATASOURCETYPE.YFINANCE,
            Ct.fundamentals_type_key(): None,
            Ct.fundamentals_options_key(): [],
            Ct.force_fundamentals_key(): False,
            Ct.indicators_key(): [],
            Ct.start_date_key(): dt.datetime(2021, 3, 7) - dt.timedelta(1825),
            Ct.end_date_key(): dt.datetime(2021, 3, 7),
            Ct.interval_key(): interval,
            Ct.period_key(): None,
            Ct.bulk_key(): True

        }

        stocks = \
            StocksFactory.create_stocks(
                conf=conf
            )

        prices_df = stocks[0].get_prices_data(keys={Ct.adj_close_key(): True})

        df = Financials.pct_change(prices_df)

        params = {Ct.interval_key(): interval}
        calmar = Calmar()
        result = calmar.calculate(df, params)

        self.assertEqual(1.1700790532917946, result[Ct.calmar_key()]['TSLA'])


    def test_KPI_volatility(self):
        tickers = ["TSLA", "SPY"]
        interval = Ct.INTERVAL.DAY

        conf = {
            Ct.tickers_key(): tickers,
            Ct.historical_type_key(): DATASOURCETYPE.YFINANCE,
            Ct.fundamentals_type_key(): None,
            Ct.fundamentals_options_key(): [],
            Ct.force_fundamentals_key(): False,
            Ct.indicators_key(): [],
            Ct.start_date_key(): dt.datetime(2021, 3, 7) - dt.timedelta(1825),
            Ct.end_date_key(): dt.datetime(2021, 3, 7),
            Ct.interval_key(): interval,
            Ct.period_key(): None,
            Ct.bulk_key(): True

        }

        stocks = \
            StocksFactory.create_stocks(
                conf=conf
            )

        prices_df = stocks[0].get_prices_data(keys={Ct.adj_close_key(): True})

        df = Financials.pct_change(prices_df)

        params = {Ct.interval_key(): interval}
        volatility = Volatility()
        result = volatility.calculate(df, params)
        self.assertEqual(0.5807261171106989, result[Ct.volatility_key()]['TSLA'])




    def test_KPI_sharpe(self):
        tickers = ["TSLA", "SPY"]
        interval = Ct.INTERVAL.DAY

        conf = {
            Ct.tickers_key(): tickers,
            Ct.historical_type_key(): DATASOURCETYPE.YFINANCE,
            Ct.fundamentals_type_key(): None,
            Ct.fundamentals_options_key(): [],
            Ct.force_fundamentals_key(): False,
            Ct.indicators_key(): [],
            Ct.start_date_key(): dt.datetime(2021, 3, 7) - dt.timedelta(1825),
            Ct.end_date_key(): dt.datetime(2021, 3, 7),
            Ct.interval_key(): interval,
            Ct.period_key(): None,
            Ct.bulk_key(): True

        }

        stocks = \
            StocksFactory.create_stocks(
                conf=conf
            )

        prices_df = stocks[0].get_prices_data(keys={Ct.adj_close_key(): True})

        df = Financials.pct_change(prices_df)

        params = {Ct.interval_key(): interval, "rf": 0.0144}
        sharpe = Sharpe()
        result = sharpe.calculate(df, params)
        self.assertEqual(1.1967403968377064, result[Ct.sharpe_key()]['TSLA'])



    def test_KPI_sortino(self):
        tickers = ["TSLA", "SPY"]
        interval = Ct.INTERVAL.DAY

        conf = {
            Ct.tickers_key(): tickers,
            Ct.historical_type_key(): DATASOURCETYPE.YFINANCE,
            Ct.fundamentals_type_key(): None,
            Ct.fundamentals_options_key(): [],
            Ct.force_fundamentals_key(): False,
            Ct.indicators_key(): [],
            Ct.start_date_key(): dt.datetime(2021, 3, 7) - dt.timedelta(1825),
            Ct.end_date_key(): dt.datetime(2021, 3, 7),
            Ct.interval_key(): interval,
            Ct.period_key(): None,
            Ct.bulk_key(): True

        }

        stocks = \
            StocksFactory.create_stocks(
                conf=conf
            )

        prices_df = stocks[0].get_prices_data(keys={Ct.adj_close_key(): True})

        df = Financials.pct_change(prices_df)

        params = {Ct.interval_key(): interval, "rf": 0.0144}
        sortino = Sortino()
        result = sortino.calculate(df, params)
        self.assertEqual(2.071479016783677, result[Ct.sortino_key()]['TSLA'])




    @staticmethod
    def print_report(reports):
        for report in reports:
            report.print()



if __name__ == '__main__':
    unittest.main()
