from data.DataSource import DATASOURCETYPE

from data.PandasDataReaderDataSource import PandasDataReaderDataSource
from data.YFinanceDataSource import YFinanceDataSource
from data.AlphaAPIDataSource import AlphaAPIDataSource


import datetime

from utilities.Constants import Constants


class DataCollector:

    def __init__(self,
                 tickers,
                 data_source_type_historic,
                 data_source_type_fundamentals,
                 fundamentals=True,
                 historical=True,
                 start_date=datetime.date.today() - datetime.timedelta(1),
                 end_date=datetime.date.today(),
                 period=None,
                 interval=Constants.INTERVAL.DAY):

        super().__init__()

        if tickers is None:
            print("Error: Define your tickers first !!!.")
            raise ValueError

        self.data_source_historic = self.set_data_source(data_source_type_historic, tickers)
        self.data_source_fundamentals = self.set_data_source(data_source_type_fundamentals, tickers)

        self.data_source_fundamentals = None

        self.set_data_source(data_source_type_historic, tickers)

        self.start_date = None
        self.end_date = None
        self.period = None
        self.interval = None

        self.set_parameters(start_date, end_date, period, interval)

        if historical == True:
            self.extract_historical_data()

        if fundamentals == True:
            self.extract_fundamentals()


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
        if data_source_type is DATASOURCETYPE.PANDASDATAREADER:
            data_source = PandasDataReaderDataSource()

        elif data_source_type is DATASOURCETYPE.YFINANCE:
            data_source = YFinanceDataSource(tickers)

        elif data_source_type is DATASOURCETYPE.ALPHA:
            data_source = AlphaAPIDataSource(tickers)


        data_source.tickers = tickers
        return data_source


    def extract_historical_data(self):


        self.data_source_historic.extract_historical_data(
            start_date=self.start_date,
            end_date=self.end_date,
            period=self.period,
            interval=self.interval
        )

        return self.data_source_historic

    def extract_fundamentals(self):
        self.data_source_historic.extract_fundamentals()

