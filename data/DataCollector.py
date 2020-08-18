from data.DataSource import DataSource
from data.PandasDataReaderDataSource import PandasDataReaderDataSource
from data.YFinanceDataSource import YFinanceDataSource

import datetime

from utilities.Constants import Constants


class DataCollector:

    def __init__(self,
                 tickers,
                 data_source_type=DataSource.DATASOURCETYPE.YFINANCE):

        super().__init__()

        if tickers is None:
            print("Error: Define your tickers first !!!.")
            raise ValueError

        self.data_source = None
        self.set_data_source(data_source_type, tickers)



    def set_data_source(self, data_source_type):
        if data_source_type is DataSource.DATASOURCETYPE.PANDASDATAREADER:
            self.data_source = PandasDataReaderDataSource()

        elif data_source_type is DataSource.DATASOURCETYPE.YFINANCE:
            self.data_source = YFinanceDataSource()

        elif data_source_type is DataSource.DATASOURCETYPE.ALPHA:
            self.data_source = None  # TODO

        elif data_source_type is DataSource.DATASOURCETYPE.YAHOOFINANCIALS:
            self.data_source = None  # TODO



    def extract_historical_data(
            self,
            start_date=datetime.date.today() - datetime.timedelta(1),
            end_date=datetime.date.today(),
            period=None,
            interval=Constants.INTERVAL.DAY):


        self.data_source.extract_historical_data(
            self.tickers,
            start_date=start_date,
            end_date=end_date,
            period=period,
            interval=interval
        )

        return self.data_source

    def extract_fundamentals(self):
        #self.data_source.extract_fundamentals()
        pass