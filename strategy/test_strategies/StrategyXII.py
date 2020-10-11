from strategy.Strategy import Strategy
from utilities.Constants import Constants

from data.DataSource import DATASOURCETYPE
from fundamentals.Fundamentals import FUNDAMENTALSTYPE


import datetime



class StrategyXII(Strategy):

    name = "StrategyXII"

    def __init__(self):

        super().__init__()
        self.set_data_source_types()
        self.set_date_parameters()
        self.set_indicators()
        self.fundamentals_options = \
            [
                FUNDAMENTALSTYPE.OVERVIEW,
                FUNDAMENTALSTYPE.BALANCE_SHEET,
                FUNDAMENTALSTYPE.INCOME_STATEMENT,
                FUNDAMENTALSTYPE.CASH_FLOW
            ]

    def set_data_source_types(self):
        self.data_source_type_historical = None
        self.data_source_type_fundamentals = DATASOURCETYPE.ALPHA

    # If period is not None it will precede over date
    def set_date_parameters(self):
        self.period = None
        self.end_date = datetime.datetime.today()
        date_str = "11/07/2019"
        self.start_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        self.interval = Constants.INTERVAL.DAY

    def set_indicators(self):
        self.indicators = []
