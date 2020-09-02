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


    def testplot_2_only_stock(self):
        tickers = ["TSLA", "SPY"]


        strategies = [AV_STRATEGY.STRATEGYI]

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

        assert TestIndicators.truncate(stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["High"].iloc[0]) == \
               TestIndicators.truncate(309.783), \
            TestIndicators.truncate(stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["High"].iloc[0])

        assert TestIndicators.truncate(stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["Low"].iloc[0]) == \
               TestIndicators.truncate(275.201), \
            TestIndicators.truncate(stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["Low"].iloc[0])

        assert TestIndicators.truncate(stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["Open"].iloc[0]) == \
               TestIndicators.truncate(279.200), \
            stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["Open"].iloc[0]

        assert TestIndicators.truncate(stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["Close"].iloc[0]) == \
               TestIndicators.truncate(308.929), \
            TestIndicators.truncate(stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["Close"].iloc[0])

        assert stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["Volume"].iloc[0] == \
               116688000, \
            stocks_per_strategy[AV_STRATEGY.STRATEGYI.name][0].price_info["TSLA"]["Volume"].iloc[0]


        print("Analysis has been run")

        plotter = Plotter()

        for stock_list in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_list]:
                plotter.plot_stock(stock, period=500)

        plt.show()





    def test_2_macd(self):
        tickers = ["TSLA", "SPY"]

        strategies = [AV_STRATEGY.STRATEGYII]

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

        assert TestIndicators.truncate(
            stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["High"].iloc[0]) == \
               TestIndicators.truncate(309.783), \
            TestIndicators.truncate(
                stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["High"].iloc[0])

        assert TestIndicators.truncate(
            stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Low"].iloc[0]) == \
               TestIndicators.truncate(275.201), \
            TestIndicators.truncate(
                stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Low"].iloc[0])

        assert TestIndicators.truncate(
            stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Open"].iloc[0]) == \
               TestIndicators.truncate(279.200), \
            stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Open"].iloc[0]

        assert TestIndicators.truncate(
            stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Close"].iloc[0]) == \
               TestIndicators.truncate(308.929), \
            TestIndicators.truncate(
                stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Close"].iloc[0])

        assert stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Volume"].iloc[0] == \
               116688000, \
            stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Volume"].iloc[0]

        print("Analysis has been run")


        plt.show()


    def test_2_macd_plot(self):
        tickers = ["TSLA", "SNAP"]# , "SPY", "CCL"

        strategies = [AV_STRATEGY.STRATEGYII]

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

        test_date="14/07/2020"
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info

        h_value = TestIndicators.truncate(
            test_df["TSLA"]["High"].loc[
                test_df["TSLA"]["High"].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
            ].iloc[0])
        assert h_value == TestIndicators.truncate(318.0), h_value

            #
        # assert TestIndicators.truncate(record["TSLA"]["Low"]) == \
        #        TestIndicators.truncate(275.201), \
        #     TestIndicators.truncate(record["TSLA"]["Low"])
        #
        # assert TestIndicators.truncate(record["TSLA"]["Open"]) == \
        #        TestIndicators.truncate(279.200), \
        #     TestIndicators.truncate(record["TSLA"]["Open"])
        #
        # assert TestIndicators.truncate(record["TSLA"]["Close"]) == \
        #        TestIndicators.truncate(308.929), \
        #     TestIndicators.truncate(record["TSLA"]["Close"])
        #
        # assert TestIndicators.truncate(record["TSLA"]["Volume"]) == \
        #        TestIndicators.truncate(116688000), \
        #     TestIndicators.truncate(record["TSLA"]["Volume"])



        print("Analysis has been run")




        for stock_list in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_list]:
                plotter = Plotter()#TODO: make this object re-usable
                plotter.plot_stock(stock, period=500)

        plt.show()


    def test_2_macd_bulk(self):
        tickers = ["TSLA"]#, "SPY", "TSLA", "SNAP"

        strategies = [AV_STRATEGY.STRATEGYII]

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

        # assert TestIndicators.truncate(
        #     stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["High"].iloc[0]) == \
        #        TestIndicators.truncate(309.783), \
        #     TestIndicators.truncate(
        #         stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["High"].iloc[0])
        #
        # assert TestIndicators.truncate(
        #     stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Low"].iloc[0]) == \
        #        TestIndicators.truncate(275.201), \
        #     TestIndicators.truncate(
        #         stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Low"].iloc[0])
        #
        # assert TestIndicators.truncate(
        #     stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Open"].iloc[0]) == \
        #        TestIndicators.truncate(279.200), \
        #     stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Open"].iloc[0]
        #
        # assert TestIndicators.truncate(
        #     stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Close"].iloc[0]) == \
        #        TestIndicators.truncate(308.929), \
        #     TestIndicators.truncate(
        #         stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Close"].iloc[0])
        #
        # assert stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Volume"].iloc[0] == \
        #        116688000, \
        #     stocks_per_strategy[AV_STRATEGY.STRATEGYII.name][0].price_info["TSLA"]["Volume"].iloc[0]


        print("Analysis has been run")

        plotter = Plotter()

        for stock_list in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_list]:
                plotter.plot_stock(stock, period=500)

        plt.show()




    def test_macd(self):
        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 1825
        # TODO: check what is happening with period < 100
        period = 100

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        macd_ind = MACD()
        self.stock.append_indicator(macd_ind)

        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()

    def test_atr(self):
        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 365 * 3
        period = 1000

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        atr = ATR()
        self.stock.append_indicator(atr)

        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()

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

    def test_macd_atr(self):
        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        macd_ind = MACD()
        self.stock.append_indicator(macd_ind)

        atr = ATR()
        self.stock.append_indicator(atr)
        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()

    def test_bollinger_bands(self):
        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       interval=Constants.INTERVAL.DAY)

        bb = BollingerBands()
        self.stock.append_indicator(bb)

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
