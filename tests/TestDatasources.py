import unittest
from stocks_model.Stock import Stock
from data.YFinanceDataSource import YFinanceDataSource
from utilities.Constants import Constants



import pprint


class TestFundamentals(unittest.TestCase):
    apikey = "86VFFOKUNB1M9YQ8"
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True


    # def test_datasources_yahoo_api(self):
    #
    #     data_source_type = HistoricalData.DATASOURCETYPE.YAHOOAPI
    #
    #     self.tickers = ["TSLA"]#, "TSLA", "UBER"]
    #
    #
    #     self.run_analysis(data_source_type)
    #
    #     print("Analysis has been run")
    #
    #
    # def test_datasources_yahoo_financials(self):
    #
    #     data_source_type = HistoricalData.DATASOURCETYPE.YAHOOFINANCIALS
    #
    #     self.tickers = ["FB", "TSLA", "UBER"]
    #     self.run_analysis(data_source_type)


    def test_datasources_YFinance(self):

        data_source = YFinanceDataSource()

        tickers = ["TSLA"]
        # self.run_analysis(data_source_type)
        start_date = "2020-01-01"
        end_date = "2020-03-10"
        period=None
        interval = Constants.INTERVAL.DAY

        self.get_historical_data(data_source,
                                 tickers,
                                 start_date,
                                 end_date,
                                 period,
                                 interval)

        assert data_source.prices["Close"].iloc[0] == 418.3299865722656

        print("Done!")



    def test_stock_datasources_YFinance(self):

        data_source = YFinanceDataSource()

        tickers = ["TSLA"]
        # self.run_analysis(data_source_type)
        start_date = "2020-01-01"
        end_date = "2020-03-10"
        period = None
        interval = Constants.INTERVAL.DAY

        self.get_historical_data(data_source,
                                 tickers,
                                 start_date,
                                 end_date,
                                 period,
                                 interval)

        assert data_source.prices["Close"].iloc[0] == 418.3299865722656

        print("Done!")

    def run_analysis(self, data_source_type):

        self.stock = Stock(self.tickers)
        self.stock.set_data_source(data_source_type=data_source_type)

        self.get_fundamentals()



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





    def get_historical_data(self, data_source, tickers, start_date, end_date, period, interval):
        if self.historical_data:
            data_source.extract_historical_data(
                tickers,
                start_date=start_date,
                end_date=end_date,
                period=period,
                interval=interval
            )


if __name__ == '__main__':
    unittest.main()