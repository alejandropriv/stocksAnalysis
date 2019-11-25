import unittest
from PlotData import PlotData
from Stock import Stock
from data.HistoricalData import HistoricalData

import pprint


from StockPlot import StockPlot


class TestBasics(unittest.TestCase):
    apikey = "86VFFOKUNB1M9YQ8"
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None

    def test_datasources_yahoo_api(self):

        data_source_type = HistoricalData.DATASOURCETYPE.YAHOOAPI

        self.tickers = ["FB", "TSLA", "UBER"]


        self.run_analysis(data_source_type)

        print("Analysis has been run")


    def test_datasources_yahoo_financials(self):

        data_source_type = HistoricalData.DATASOURCETYPE.YAHOOFINANCIALS

        self.tickers = ["FB", "TSLA", "UBER"]
        self.run_analysis(data_source_type)




    def run_analysis(self, data_source_type):

        self.stock = Stock(self.tickers)
        self.stock.set_data_source(data_source_type=data_source_type)

        # self.get_fundamentals()

        self.get_historical_data()



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
