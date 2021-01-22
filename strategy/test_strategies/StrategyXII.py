from strategy.Strategy import Strategy
from utilities.Constants import Constants

from data.DataSource import DATASOURCETYPE
from fundamentals.Fundamentals import FUNDAMENTALSTYPE

from value_investment.MagicFormula import MagicFormula


import datetime



class StrategyXII(Strategy):

    name = "StrategyXII"

    def __init__(self):

        super().__init__()
        self.set_data_source_types()
        self.set_date_parameters()
        self.set_indicators()
        self.set_value_investing_metrics()
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

    # TODO: Right now date do not affect fundamentals
    # If period is not None it will precede over date
    def set_date_parameters(self):
        self.period = None
        self.end_date = "31/3/2020"
        date_str = "11/07/2019"
        self.start_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        self.interval = Constants.INTERVAL.DAY

    def set_indicators(self):
        self.indicators = []

    def set_value_investing_metrics(self):
        magic_formula = MagicFormula()
        self.value_investing_metrics = [magic_formula]
