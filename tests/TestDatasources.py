import unittest
from data.YFinanceDataSource import YFinanceDataSource
from utilities.Constants import Constants


class TestFundamentals(unittest.TestCase):
    apikey = "86VFFOKUNB1M9YQ8"
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True


    def test_datasources_YFinance(self):

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

        assert data_source.prices["TSLA"]["Adj Close"].iloc[0] == 83.66600036621094

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
