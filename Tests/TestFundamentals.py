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


    def test_fundamentals(self):

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
