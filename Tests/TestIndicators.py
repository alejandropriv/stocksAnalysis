import unittest

import matplotlib.pyplot as plt

from Stock import Stock
from indicators.ATR import ATR
from indicators.MACD import MACD
from indicators.RSI import RSI
from indicators.ADX import ADX
from indicators.OBV import OBV

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

    def test_macd(self):
        self.tickers = ["CCL"]  # , "TSLA", "UBER"]

        past_date_interval = 1825
        period = 50

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

        self.stock.plot(period=period)


        self.calculate_bollinger_bands(period=period, plotter=self.stock.plotter)


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
        self.stock.plot(period=period)

        self.calculate_bollinger_bands(period=period, plotter=self.stock.plotter)

        # added these three lines
        # lns1 = ax.plot(time, Swdown, '-', label = 'Swdown')

        # lns = lns1 + lns2 + lns3
        # labs = [l.get_label() for l in lns]
        # ax.legend(lns, labs, loc=0)

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
        self.stock.plot(period=period)

        self.stock.plotter = self.calculate_bollinger_bands(period=period, plotter=self.stock.plotter)

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

        self.stock.plot(period=period)

        self.calculate_macd(period=period)
        self.stock.plotter = self.calculate_atr(period=period, plotter=self.stock.plotter)

        self.stock.plotter = self.calculate_bollinger_bands(period=period, plotter=self.stock.plotter)

        # todo put this in a different subplot
        self.stock.plotter = self.calculate_rsi(period=period, plotter=self.stock.plotter)

        # added these three lines
        # lns1 = ax.plot(time, Swdown, '-', label = 'Swdown')

        # lns = lns1 + lns2 + lns3
        # labs = [l.get_label() for l in lns]
        # ax.legend(lns, labs, loc=0)

        print("Analysis has been run")

        plt.show()





    ###################################################################
    #  CALCULATIONS
    ###################################################################
    def calculate_rsi(self, period=100, plotter=None):
        self.get_historical_data()

        prices = self.stock.get_prices_data(tickers=self.tickers,
                                            has_high_key=False,
                                            has_low_key=False,
                                            has_adj_close_key=True,
                                            has_volume_key=False)

        prices.ticker = self.tickers[0]

        rsi_ind = RSI(df=prices, n=14, plotter=plotter)
        rsi_ind.calculate()

        # The period is determined by the TIMESERIES chosen
        rsi_ind.plot(period=period, color="tab:purple")

        return rsi_ind.plotter


    def calculate_bollinger_bands(self, period=100, plotter=None):
        self.get_historical_data()

        price_close_adj = self.stock.get_prices_data(tickers=self.tickers,
                                                     has_high_key=False,
                                                     has_low_key=False,
                                                     has_adj_close_key=True,
                                                     has_volume_key=False)

        price_close_adj.ticker = self.tickers[0]

        bb_ind = BollingerBands(df=price_close_adj, n=20)
        bb_ind.calculate()

        bb_ind.plot(plotter=plotter, period=period, color="tab:red")

        return plotter

    def get_historical_data(self):
        if self.historical_data:
            self.stock.get_historical_data()



if __name__ == '__main__':
    unittest.main()
