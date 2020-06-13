import unittest

import matplotlib.pyplot as plt

from Stock import Stock
from indicators.ATR import ATR
from indicators.MACD import MACD
from indicators.RSI import RSI
from indicators.ADX import ADX
from indicators.OBV import OBV
from indicators.RENKO import RENKOIND

from indicators.Slope import Slope


from indicators.BollingerBands import BollingerBands
from utilities.Constants import Constants

import datetime


class TestBasics(unittest.TestCase):
    apikey = "86VFFOKUNB1M9YQ8"
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None

    def testplot_only_stock(self):
        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 1825
        # TODO: check what is happening with period < 100
        period = 100

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       time_series=Constants.TIMESERIES.DAILY)


        self.stock.plot(period=period)

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
                                       time_series=Constants.TIMESERIES.DAILY)

        macd_ind = MACD()
        self.stock.append_indicator(macd_ind)

        self.stock.plot(period=period)

        print("Analysis has been run")

        plt.show()




    def test_atr(self):
        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 365*3
        period = 1000

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       time_series=Constants.TIMESERIES.DAILY)

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
                                       time_series=Constants.TIMESERIES.DAILY)

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
                                       time_series=Constants.TIMESERIES.DAILY)


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
                                       time_series=Constants.TIMESERIES.DAILY)

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
                                       time_series=Constants.TIMESERIES.DAILY)

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
                                       time_series=Constants.TIMESERIES.DAILY)


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
                                       time_series=Constants.TIMESERIES.DAILY)


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
                                       time_series=Constants.TIMESERIES.DAILY)

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
                                       time_series=Constants.TIMESERIES.DAILY)


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
                                       time_series=Constants.TIMESERIES.DAILY)

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
