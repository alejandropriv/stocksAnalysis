from strategy.Strategy import Strategy
from utilities.Constants import Constants

from data.DataSource import DATASOURCETYPE
from kpi.Volatility import Volatility

import datetime


class StrategyXXX(Strategy):
    name = "StrategyXXX"

    def __init__(self):
        super().__init__()
        self.set_data_source_types()
        self.set_date_parameters()
        self.set_indicators()
        self.set_method()

    def set_data_source_types(self):
        self.dst_historical = DATASOURCETYPE.YFINANCE
        self.dst_fundamentals = None

    # If period is not None it will precede over date

    def set_date_parameters(self):
        self.period = None
        date_end_str = "01/01/2020"
        self.end_date = datetime.datetime.strptime(date_end_str, "%d/%m/%Y")
        date_start_str = "01/01/2010"
        self.start_date = datetime.datetime.strptime(date_start_str, "%d/%m/%Y")
        self.interval = Constants.INTERVAL.DAY

    def set_indicators(self):
        self.indicators = []

    def set_method(self):
        pass
