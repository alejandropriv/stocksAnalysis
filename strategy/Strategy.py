import abc
from data.DataSource import DATASOURCETYPE
from fundamentals.Fundamentals import FUNDAMENTALSTYPE


class Strategy(metaclass=abc.ABCMeta):

    def __init__(self):

        self.data_source_type_historical = None
        self.data_source_type_fundamentals = None
        self.period = None
        self.start_date = None
        self.end_date = None
        self.interval = None
        self.indicators = []
        self.kpis = []
        self.data_source_type_fundamentals = False
        self.fundamentals_options = [FUNDAMENTALSTYPE.BALANCE_SHEET,
                                     FUNDAMENTALSTYPE.INCOME_STATEMENT,
                                     FUNDAMENTALSTYPE.CASH_FLOW]
        self.value_investing_metrics = []

        self.kpis = []

        # 0: run the normal flow
        # 1: force new data to be requested from server
        # 2. force cached data
        self.force_fundamentals = 0

        # Force bulk- i.e. Magic formula
        self.bulk = None

    @abc.abstractmethod
    def set_data_source_types(self):
        self.data_source_type_historical = DATASOURCETYPE.YFINANCE
        self.data_source_type_fundamentals = DATASOURCETYPE.ALPHA

    def set_date_parameters(self):
        pass



