import unittest

import matplotlib.pyplot as plt

from Stock import Stock
from indicators.ATR import ATR
from indicators.MACD import MACD
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

        self.stock = Stock(self.tickers)

        self.calculate_atr(ticker="FB")

        print("Analysis has been run")

    def test_macd_atr(self):
        self.tickers = ["FB"]  # , "TSLA", "UBER"]

        self.stock = Stock(self.tickers)

        plotter = self.calculate_macd()

        plotter = self.calculate_atr(plotter=plotter)

        # added these three lines
        # lns1 = ax.plot(time, Swdown, '-', label = 'Swdown')

        # lns = lns1 + lns2 + lns3
        # labs = [l.get_label() for l in lns]
        # ax.legend(lns, labs, loc=0)

        print("Analysis has been run")

        plt.show()

    def test_macd_bollinger_bands(self):
        self.tickers = ["FB"]  # , "TSLA", "UBER"]

        period = 150
        self.stock = Stock(self.tickers)

        plotter = self.calculate_macd(period=period)

        plotter = self.calculate_bollinger_bands(period=period, plotter=plotter)

        # added these three lines
        # lns1 = ax.plot(time, Swdown, '-', label = 'Swdown')

        # lns = lns1 + lns2 + lns3
        # labs = [l.get_label() for l in lns]
        # ax.legend(lns, labs, loc=0)

        print("Analysis has been run")

        plt.show()

    def calculate_macd(self, ticker=None, period=100, plotter=None):

        self.get_historical_data()

        price_close_adj = self.stock.get_prices_data(tickers=self.tickers, has_adj_close_key=True, has_volume_key=False)
        price_close_adj.ticker = ticker

        macd_ind = MACD(price=price_close_adj, plotter=plotter)

        df = macd_ind.calculate()

        # The period is determined by the TIMESERIES chosen
        macd_ind.plot_macd(df=df, period=period)

        return macd_ind.plotter

    def calculate_atr(self, period=100, plotter=None):

        self.get_historical_data()

        prices = self.stock.get_prices_data(tickers=self.tickers,
                                            has_high_key=True,
                                            has_low_key=True,
                                            has_adj_close_key=True,
                                            has_volume_key=False)

        atr_ind = ATR(low=price_low, high=price_high, adj_close=price_close_adj, n=14, plotter=plotter)
        df = atr_ind.calculate()

        # The period is determined by the TIMESERIES chosen
        atr_ind.plot_atr(df=df, period=200, ticker=ticker, color="tab:red")

        return atr_ind.plotter

    def calculate_bollinger_bands(self, period=100, plotter=None):

        ticker = "FB"

        self.get_historical_data()

        price_close_adj = self.stock.get_prices_close_adj().iloc[:, [0]]

        bb_ind = BollingerBands(adj_close=price_close_adj, n=20, plotter=plotter)
        df = bb_ind.calculate()

        volume_key = "{}_{}".format(ticker, "Volume")

        df[volume_key] = self.stock.get_volume().iloc[:, [0]]
        # The period is determined by the TIMESERIES chosen
        bb_ind.plot_bollinger_bands(df=df, period=period, color="tab:red")

        return bb_ind.plotter

    def get_fundamentals(self):

        if self.fundamentals:
            self.stock.get_fundamentals()

            pp = pprint.PrettyPrinter(indent=4)

            for ticker, data in self.stock.fundamentals.items():
                print("--------- TICKER: {} ----------------".format(ticker))
                print("--------- INCOME STATEMENT: {} ----------------".format(ticker))
                pp.pprint(data.income_statement.get_data())

                print("--------- BALANCE SHEET: {} ----------------".format(ticker))
                pp.pprint(data.balance_sheet.get_data())

                print("--------- CASH FLOW: {} ----------------".format(ticker))
                pp.pprint(data.cash_flow.get_data())

    def get_historical_data(self):
        if self.historical_data:
            self.stock.get_historical_data()


if __name__ == '__main__':
    unittest.main()
