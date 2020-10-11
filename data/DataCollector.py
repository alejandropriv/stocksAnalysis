from data.DataSource import DATASOURCETYPE

from data.YFinanceDataSource import YFinanceDataSource
from data.AlphaAPIDataSource import AlphaAPIDataSource


import datetime

from utilities.Constants import Constants


class DataCollector:

    def __init__(self, tickers, strategy):

        super().__init__()

        if tickers is None:
            print("Error: Define your tickers first !!!.")
            raise ValueError

        self.data_source_historical = self.set_data_source(strategy.data_source_type_historical, tickers)
        self.data_source_fundamentals = self.set_data_source(strategy.data_source_type_fundamentals, tickers)

        self.start_date = None
        self.end_date = None
        self.period = None
        self.interval = None

        self.set_parameters(strategy.start_date, strategy.end_date, strategy.period, strategy.interval)



    def set_parameters(
            self,
            start_date=datetime.date.today() - datetime.timedelta(1),
            end_date=datetime.date.today(),
            period=None,
            interval=Constants.INTERVAL.DAY
    ):

        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.interval = interval



    @staticmethod
    def set_data_source(data_source_type, tickers):

        if data_source_type is DATASOURCETYPE.YFINANCE:
            data_source = YFinanceDataSource(tickers)

        elif data_source_type is DATASOURCETYPE.ALPHA:
            data_source = AlphaAPIDataSource(tickers)

        else:
            return None


        data_source.tickers = tickers
        return data_source


    def extract_historical_data(self):


        self.data_source_historical.extract_historical_data(
            start_date=self.start_date,
            end_date=self.end_date,
            period=self.period,
            interval=self.interval
        )

        return self.data_source_historical

    def extract_fundamentals(self):
        self.data_source_fundamentals.extract_fundamentals()
        return self.data_source_fundamentals

