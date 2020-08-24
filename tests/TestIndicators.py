import unittest

import matplotlib.pyplot as plt

from data.DataSource import DATASOURCETYPE

from strategy.StrategyManager import StrategyManager
from strategy.StrategyManager import AV_STRATEGY

from stocks_model.StocksFactory import StocksFactory
from stocks_model.Stock import Stock
from indicators.ATR import ATR
from indicators.MACD import MACD
from indicators.ADX import ADX
from indicators.OBV import OBV
from indicators.RENKOIND import RENKOIND

from indicators.Slope import Slope

from indicators.BollingerBands import BollingerBands
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

    def testplot_2_only_stock_old(self):
        tickers = ["TSLA", "SPY"]

        date_str = "11/07/2020"
        start_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        end_date = datetime.datetime.today()


        stocks = StocksFactory.create_stocks(tickers=tickers,
                                             data_source_type=DATASOURCETYPE.YFINANCE,
                                             start_date=start_date,
                                             end_date=end_date,
                                             period=None,
                                             interval=Constants.INTERVAL.DAY
                                             )

        for stock in stocks:
            print(stock.price_info)

        assert TestIndicators.truncate(stocks[0].price_info["High"].iloc[0]) == \
               TestIndicators.truncate(1548.920044), \
            TestIndicators.truncate(stocks[0].price_info["High"].iloc[0])

        assert TestIndicators.truncate(stocks[0].price_info["Low"].iloc[0]) == \
               TestIndicators.truncate(1376.010010), \
            TestIndicators.truncate(stocks[0].price_info["Low"].iloc[0])

        assert stocks[0].price_info["Open"].iloc[0] == \
               1396.0, \
            stocks[0].price_info["Open"].iloc[0]

        assert TestIndicators.truncate(stocks[0].price_info["Close"].iloc[0]) == \
               TestIndicators.truncate(1544.650024), \
            TestIndicators.truncate(stocks[0].price_info["Close"].iloc[0])

        assert stocks[0].price_info["Volume"].iloc[0] == \
               23337600, \
            stocks[0].price_info["Volume"].iloc[0]


        print("Analysis has been run")

        plt.show()


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

        assert TestIndicators.truncate(stocks_per_strategy[0][0].price_info["High"].iloc[0]) == \
               TestIndicators.truncate(1548.920044), \
            TestIndicators.truncate(stocks_per_strategy[0][0].price_info["High"].iloc[0])

        assert TestIndicators.truncate(stocks[0].price_info["Low"].iloc[0]) == \
               TestIndicators.truncate(1376.010010), \
            TestIndicators.truncate(stocks[0].price_info["Low"].iloc[0])

        assert stocks[0].price_info["Open"].iloc[0] == \
               1396.0, \
            stocks[0].price_info["Open"].iloc[0]

        assert TestIndicators.truncate(stocks[0].price_info["Close"].iloc[0]) == \
               TestIndicators.truncate(1544.650024), \
            TestIndicators.truncate(stocks[0].price_info["Close"].iloc[0])

        assert stocks[0].price_info["Volume"].iloc[0] == \
               23337600, \
            stocks[0].price_info["Volume"].iloc[0]


        print("Analysis has been run")

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
