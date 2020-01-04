import unittest

import matplotlib.pyplot as plt

from Stock import Stock
from indicators.ATR import ATR
from indicators.MACD import MACD
from indicators.RSI import RSI


from indicators.BollingerBands import BollingerBands
from utilities.Constants import Constants

import datetime
import pprint


class TestBasics(unittest.TestCase):
    apikey = "86VFFOKUNB1M9YQ8"
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None

    def test_macd(self):

        self.tickers = ["FB"]  # , "TSLA", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       time_series=Constants.TIMESERIES.DAILY)

        self.stock.plot(period=period)

        self.calculate_macd(period=period, plotter=self.stock.plotter)

        print("Analysis has been run")

        plt.show()

    def test_atr(self):

        self.tickers = ["FB"]  # , "TSLA", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       time_series=Constants.TIMESERIES.DAILY)

        self.stock.plot(period=period)

        self.calculate_atr(period=period, plotter=self.stock.plotter)

        print("Analysis has been run")

        plt.show()


    def test_adx(self):

        self.tickers = ["FB"]  # , "TSLA", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       time_series=Constants.TIMESERIES.DAILY)

        self.stock.plot(period=period)

        self.calculate_adx(period=period, plotter=self.stock.plotter)

        print("Analysis has been run")

        plt.show()

    def test_macd_atr(self):

        self.tickers = ["FB"]  # , "TSLA", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       time_series=Constants.TIMESERIES.DAILY)

        self.stock.plot(period=period)

        self.stock.plotter = self.calculate_macd(period=period, plotter=self.stock.plotter)
        self.calculate_atr(period=period, plotter=self.stock.plotter)

        print("Analysis has been run")

        plt.show()

    def test_rsi(self):

        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       time_series=Constants.TIMESERIES.DAILY)

        self.stock.plot(period=period)

        #self.stock.plotter = self.calculate_macd(period=period, plotter=self.stock.plotter)
        self.calculate_rsi(period=period, plotter=self.stock.plotter)

        print("Analysis has been run")

        plt.show()


    def test_macd_atr_bollinger_bands(self):
        self.tickers = ["TSLA"]  # , "FB", "UBER"]

        past_date_interval = 365
        period = 200

        self.stock = Stock(self.tickers)

        self.stock.get_historical_data(start_date=datetime.date.today() - datetime.timedelta(past_date_interval),
                                       end_date=(datetime.date.today()),
                                       time_series=Constants.TIMESERIES.DAILY)

        self.stock.plot(period=period)

        self.stock.plotter = self.calculate_macd(period=period, plotter=self.stock.plotter)
        self.stock.plotter = self.calculate_atr(period=period, plotter=self.stock.plotter)


        self.stock.plotter = self.calculate_bollinger_bands(period=period, plotter=self.stock.plotter)

        # added these three lines
        # lns1 = ax.plot(time, Swdown, '-', label = 'Swdown')

        # lns = lns1 + lns2 + lns3
        # labs = [l.get_label() for l in lns]
        # ax.legend(lns, labs, loc=0)

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

        self.stock.plotter = self.calculate_macd(period=period, plotter=self.stock.plotter)
        self.stock.plotter = self.calculate_atr(period=period, plotter=self.stock.plotter)


        self.stock.plotter = self.calculate_bollinger_bands(period=period, plotter=self.stock.plotter)


        #todo put this in a different subplot
        self.stock.plotter = self.calculate_rsi(period=period, plotter=self.stock.plotter)

        # added these three lines
        # lns1 = ax.plot(time, Swdown, '-', label = 'Swdown')

        # lns = lns1 + lns2 + lns3
        # labs = [l.get_label() for l in lns]
        # ax.legend(lns, labs, loc=0)

        print("Analysis has been run")

        plt.show()

    def calculate_macd(self, period=100, plotter=None):

        self.get_historical_data()

        price_close_adj = self.stock.get_prices_data(tickers=self.tickers, has_adj_close_key=True, has_volume_key=False)
        price_close_adj.ticker = self.tickers[0]

        macd_ind = MACD(df=price_close_adj, plotter=plotter)

        macd_ind.calculate()

        # The period is determined by the TIMESERIES chosen
        macd_ind.plot(period=period)

        return macd_ind.plotter




    def calculate_atr(self, period=100, plotter=None):

        self.get_historical_data()

        prices = self.stock.get_prices_data(tickers=self.tickers,
                                            has_high_key=True,
                                            has_low_key=True,
                                            has_adj_close_key=True,
                                            has_volume_key=False)

        prices.ticker = self.tickers[0]

        atr_ind = ATR(df=prices, n=14, plotter=plotter)
        atr_ind.calculate()

        # The period is determined by the TIMESERIES chosen
        atr_ind.plot(period=period, color="tab:red")

        return atr_ind.plotter


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



    def calculate_adx(self, period=100, plotter=None):

        self.get_historical_data()

        prices = self.stock.get_prices_data(tickers=self.tickers,
                                            has_high_key=True,
                                            has_low_key=True,
                                            has_adj_close_key=True,
                                            has_volume_key=False)

        prices.ticker = self.tickers[0]

        ind = ADX(df=prices, n=14, plotter=plotter)
        ind.calculate()

        # The period is determined by the TIMESERIES chosen
        ind.plot(period=period, color="tab:pink")

        return ind.plotter


    def calculate_bollinger_bands(self, period=100, plotter=None):

        self.get_historical_data()

        price_close_adj = self.stock.get_prices_data(tickers=self.tickers,
                                                     has_high_key=False,
                                                     has_low_key=False,
                                                     has_adj_close_key=True,
                                                     has_volume_key=False)

        price_close_adj.ticker = self.tickers[0]

        bb_ind = BollingerBands(df=price_close_adj, n=20, plotter=plotter)
        bb_ind.calculate()

        bb_ind.plot(period=period, color="tab:red")

        return bb_ind.plotter


    def get_historical_data(self):
        if self.historical_data:
            self.stock.get_historical_data()


if __name__ == '__main__':
    unittest.main()
