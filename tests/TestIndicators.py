import unittest

import matplotlib.pyplot as plt


from strategy.StrategyManager import StrategyManager

from strategy.test_strategies.StrategyII import StrategyII
from strategy.test_strategies.StrategyIII import StrategyIII
from strategy.test_strategies.StrategyIV import StrategyIV
from strategy.test_strategies.StrategyV import StrategyV
from strategy.test_strategies.StrategyVI import StrategyVI
from strategy.test_strategies.StrategyVII import StrategyVII
from strategy.test_strategies.StrategyVIII import StrategyVIII
from strategy.test_strategies.StrategyIX import StrategyIX

from strategy.test_strategies.StrategyC import StrategyC
from strategy.test_strategies.StrategyCI import StrategyCI
from strategy.test_strategies.StrategyCII import StrategyCII
from strategy.test_strategies.StrategyCIII import StrategyCIII


from plotter.Plotter import Plotter

import datetime




DEVELOPMENT = True

class TestIndicators(unittest.TestCase):
    apikey = "86VFFOKUNB1M9YQ8"
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None
    stocks_factory = None


    @staticmethod
    def truncate(n):
        return int(n * 1000) / 1000


    def test_macd_no_plot(self):
        tickers = ["TSLA", "SPY"]

        strategies = [StrategyIII()]

        smanager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = smanager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)


        if DEVELOPMENT == True:
            plt.show()



        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyIII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


        print("Analysis has been run")


    def test_bollinger_bands(self):
        tickers = ["TSLA", "SNAP"]

        strategies = [StrategyII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=True)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_bollinger_bands_bulk(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1



    def test_macd(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyIII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=500)
                plotter.plot_stock(stock)


        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()



        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyIII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_macd_collapse(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyIII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=500)
                plotter.plot_stock(stock, collapse_indicators=True)


        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()



        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyIII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1



    def test_macd_bulk(self):
        tickers = ["TSLA"]  # , "SPY", "TSLA", "SNAP"

        strategies = [StrategyIII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=500)
                plotter.plot_stock(stock)


        print("Analysis has been run")


        if DEVELOPMENT == True:
            plt.show()



        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyIII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_atr(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyIV()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,

            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=500)
                plotter.plot_stock(stock)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyIV.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_atr_bulk(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyIV()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True

            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=500)
                plotter.plot_stock(stock)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyIV().name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_rsi(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyV()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyV.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_rsi_bulk(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyV()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyV.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_adx(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyVI()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyVI.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_adx_bulk(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyVI()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyVI.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_obv(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyVII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyVII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_obv_bulk(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyVII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyVII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_slope(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyIX()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyIX.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1



    def test_renko(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyVIII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyVIII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1



    def test_renko_macd(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyCIII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyCIII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_macd_rsi(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyCI()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyCI.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1



    def test_macd_rsi_collapse(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyCI()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=True)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyCI.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_macd_atr_collapse(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyC()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyC.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_macd_atr(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyC()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyC().name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1

    def test_macd_rsi_adx_atr_obv_bb_collapse(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyCII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=True)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyCII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


    def test_macd_rsi_adx_atr_obv_bb(self):
        tickers = ["TSLA", "SNAP"]

        strategies = [StrategyCII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[StrategyCII.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1



if __name__ == '__main__':
    unittest.main()
