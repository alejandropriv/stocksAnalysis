from data.DataSource import DATASOURCETYPE

from data.YFinanceDataSource import YFinanceDataSource
from data.AlphaAPIDataSource import AlphaAPIDataSource



class DataCollector:

    HISTORICAL_KEY = "historical"
    FUNDAMENTALS_KEY = "fundamentals"



    @staticmethod
    def set_data_source(data_source_type):

        if data_source_type is DATASOURCETYPE.YFINANCE:
            data_source = YFinanceDataSource()

        elif data_source_type is DATASOURCETYPE.ALPHA:
            data_source = AlphaAPIDataSource()

        else:
            return None

        return data_source


    @staticmethod
    def get_data_sources(data_source_type_historical, data_source_type_fundamentals):
        data_sources = dict()

        data_sources[DataCollector.HISTORICAL_KEY] = DataCollector.set_data_source(data_source_type_historical)
        data_sources[DataCollector.FUNDAMENTALS_KEY] = DataCollector.set_data_source(data_source_type_fundamentals)

        return data_sources
