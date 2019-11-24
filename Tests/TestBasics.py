import unittest
from PlotData import PlotData
from Stock import Stock
from data.DataSource import DataSource

import pprint


from StockPlot import StockPlot


class TestBasics(unittest.TestCase):
    apikey = "86VFFOKUNB1M9YQ8"
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    def test_datasources_yahoo_api(self):

        data_source_type = DataSource.DATASOURCETYPE.YAHOOAPI

        self.tickers = ["FB", "TSLA", "UBER"]
        self.run_analysis(data_source_type)


    def test_datasources_yahoo_financials(self):

        data_source_type = DataSource.DATASOURCETYPE.YAHOOFINANCIALS

        self.tickers = ["FB", "TSLA", "UBER"]
        self.run_analysis(data_source_type)




    def run_analysis(self, data_source_type):

        stock = Stock(self.tickers)
        stock.set_data_source(data_source_type=data_source_type)

        # self.get_fundamentals(stock)

        self.get_historical_data(stock)



    def get_fundamentals(self, stock):

        if self.fundamentals:
            stock.get_fundamentals()

            pp = pprint.PrettyPrinter(indent=4)


            for ticker, data in stock.fundamentals.items():

                print("--------- TICKER: {} ----------------".format(ticker))
                print("--------- INCOME STATEMENT: {} ----------------".format(ticker))
                pp.pprint(data.income_statement.get_data())

                print("--------- BALANCE SHEET: {} ----------------".format(ticker))
                pp.pprint(data.balance_sheet.get_data())

                print("--------- CASH FLOW: {} ----------------".format(ticker))
                pp.pprint(data.cash_flow.get_data())





    def get_historical_data(self, stock):
        if self.historical_data:
            stock.get_historical_data()


if __name__ == '__main__':
    unittest.main()
