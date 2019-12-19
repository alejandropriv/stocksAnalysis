import unittest

import matplotlib.pyplot as plt


from Stock import Stock
from indicators.ATR import ATR
from indicators.MACD import MACD


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


    def test_ATR(self):

        self.tickers = ["FB", "TSLA", "UBER"]

        self.stock = Stock(self.tickers)


        self.calculate_atr()

        print("Analysis has been run")






    def test_MACD_ATR(self):
        self.tickers = ["FB", "TSLA", "UBER"]

        self.stock = Stock(self.tickers)

        plotter = self.calculate_macd()

        plotter = self.calculate_atr(plotter=plotter)

        # added these three lines
        #lns1 = ax.plot(time, Swdown, '-', label = 'Swdown')

        #lns = lns1 + lns2 + lns3
        #labs = [l.get_label() for l in lns]
        #ax.legend(lns, labs, loc=0)

        print("Analysis has been run")

        plt.show()



    def calculate_macd(self, plotter=None):

        ticker = "FB"

        self.get_historical_data()

        price_close_adj = self.stock.get_prices_close_adj().iloc[:, [0]]

        macd_ind = MACD(price=price_close_adj, plotter=plotter)

        df = macd_ind.calculate()

        volume_key = "{}_{}".format(ticker, "Volume")


        df[volume_key] = self.stock.get_volume().iloc[:, [0]]

        # The period is determined by the TIMESERIES chosen
        macd_ind.plot_macd(df=df, period=200, ticker=ticker)

        return macd_ind.plotter



    def calculate_atr(self, plotter=None):

        ticker = "FB"

        self.get_historical_data()

        price_close_adj = self.stock.get_prices_close_adj().iloc[:, [0]]
        price_high = self.stock.get_prices_high().iloc[:, [0]]
        price_low = self.stock.get_prices_low().iloc[:, [0]]


        atr_ind = ATR(low=price_low, high=price_high, adj_close=price_close_adj, n=14, plotter=plotter)
        df = atr_ind.calculate()

        volume_key = "{}_{}".format(ticker, "Volume")


        df[volume_key] = self.stock.get_volume().iloc[:, [0]]
        # The period is determined by the TIMESERIES chosen
        atr_ind.plot_atr(df=df, period=200, ticker=ticker, color="tab:red")


        return atr_ind.plotter





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
