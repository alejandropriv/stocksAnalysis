import unittest
from Stock import Stock
from indicators.MACD import MACD
from plotter.Plotter import Plotter

import pprint


class TestBasics(unittest.TestCase):
    apikey = "86VFFOKUNB1M9YQ8"
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None

    def test_MACD(self):

        self.tickers = ["FB", "TSLA", "UBER"]

        self.stock = Stock(self.tickers)


        self.calculate_macd()

        print("Analysis has been run")



    def calculate_macd(self):

        self.get_historical_data()

        price_close_adj = self.stock.get_prices_close_adj().iloc[:, [0]]
        volume = self.stock.get_volume()

        macd_ind = MACD(price=price_close_adj)

        df = macd_ind.calculate()

        df["Volume"] = volume.iloc[:, [0]]



        # The period is determined by the TIMESERIES chosen
        Plotter.plot_macd(df, 200)






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
