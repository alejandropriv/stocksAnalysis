import unittest

import matplotlib.pyplot as plt

from data.DataSource import DATASOURCETYPE

from strategy.StrategyManager import StrategyManager
from strategy.StrategyManager import AV_STRATEGY


from stocks_model.Stock import Stock
from indicators.ATR import ATR
from indicators.MACD import MACD
from indicators.ADX import ADX
from indicators.OBV import OBV
from indicators.RENKOIND import RENKOIND

from indicators.Slope import Slope

from indicators.BollingerBands import BollingerBands

from plotter.Plotter import Plotter

from utilities.Constants import Constants

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

    def testplot_only_stock(self):
        self.tickers = ["TSLA"]

        past_date_interval = 365
        # TODO: check what is happening with period < 100
        period = 100

        date_str = "11/07/2020"
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y")

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=date,
                                       end_date=(datetime.datetime.today()),
                                       interval=Constants.INTERVAL.DAY)

        print(self.stock.price_info)
        # self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()

    @staticmethod
    def truncate(n):
        return int(n * 1000) / 1000


    def test_macd(self):
        tickers = ["TSLA", "SPY"]

        strategies = [AV_STRATEGY.STRATEGYMACD]

        smanager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE
            )

        stocks_per_strategy = smanager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)


        if DEVELOPMENT == True:
            plt.show()



        test_date = "14/07/2020"
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYMACD.name][0].price_info
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



    def test_macd_plot(self):
        tickers = ["TSLA", "SNAP"]# , "SPY", "CCL"

        strategies = [AV_STRATEGY.STRATEGYMACD]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYMACD.name][0].price_info
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
        tickers = ["TSLA"]#, "SPY", "TSLA", "SNAP"

        strategies = [AV_STRATEGY.STRATEGYMACD]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE,
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYMACD.name][0].price_info
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

        strategies = [AV_STRATEGY.STRATEGYATR]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE,
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYATR.name][0].price_info
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

        strategies = [AV_STRATEGY.STRATEGYATR]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE,
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYATR.name][0].price_info
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

        strategies = [AV_STRATEGY.STRATEGYX]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYX.name][0].price_info
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

        strategies = [AV_STRATEGY.STRATEGYX]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYX.name][0].price_info
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

        strategies = [AV_STRATEGY.STRATEGYRSI]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYRSI.name][0].price_info
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

        strategies = [AV_STRATEGY.STRATEGYRSI]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE,
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYRSI.name][0].price_info
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

        strategies = [AV_STRATEGY.STRATEGYMACDRSI]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYMACDRSI.name][0].price_info
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

        strategies = [AV_STRATEGY.STRATEGYMACDRSI]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYMACDRSI.name][0].price_info
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


    def test_bollinger_bands(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [AV_STRATEGY.STRATEGYBB]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type=DATASOURCETYPE.YFINANCE
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
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYMACDRSI.name][0].price_info
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
        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 365

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        adx = ADX()
        self.stock.append_indicator(adx)
        self.stock.plot()

        print("Analysis has been run")

        plt.show()

    def test_obv(self):
        self.tickers = ["TSLA"]  # "FB", "TSLA", "UBER"]

        past_date_interval = 365
        period = 300

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        obv = OBV()
        self.stock.append_indicator(obv)
        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()

    def test_slope(self):
        self.tickers = ["AAPL"]

        past_date_interval = 365
        period = 50

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        slope = Slope()

        self.stock.append_indicator(slope)

        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()




    def test_atr_bollinger_bands(self):
        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        atr = ATR()
        self.stock.append_indicator(atr)

        bb = BollingerBands()
        self.stock.append_indicator(bb)

        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()

    def test_macd_atr_bollinger_bands(self):
        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        self.stock.plot(period=period)

        macd_ind = MACD()
        self.stock.append_indicator(macd_ind)

        atr = ATR()
        self.stock.append_indicator(atr)

        bb = BollingerBands()
        self.stock.append_indicator(bb)

        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()

    def test_macd_atr_rsi_bollinger_bands(self):
        self.tickers = ["TSLA"]  # , "FB", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        self.stock.append_indicator(MACD())

        self.stock.append_indicator(ATR())

        bb = BollingerBands()
        self.stock.append_indicator(bb)

        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()

    def test_renko(self):
        self.tickers = ["TSLA"]  # , "FB", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        keys = {'has_high_key': True,
                'has_low_key': True,
                'has_open_key': True,
                'has_close_key': True,
                'has_adj_close_key': True,
                'has_volume_key': False
                }

        renko = RENKOIND()
        self.stock.append_indicator(renko, keys=keys)

        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()

    ###################################################################
    #  CALCULATIONS
    ###################################################################

    def get_historical_data(self):
        if self.historical_data:
            self.stock.get_historical_data()


if __name__ == '__main__':
    unittest.main()
