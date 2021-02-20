from strategy.Strategy import Strategy
from utilities.Constants import Constants

from data.DataSource import DATASOURCETYPE
from kpi.Sortino import Sortino

import datetime


class StrategyXXV(Strategy):
    name = "StrategyXXV"

    def __init__(self):
        super().__init__()
        self.set_data_source_types()
        self.set_date_parameters()
        self.set_indicators()
        self.set_kpi()

    def set_data_source_types(self):
        self.data_source_type_historical = DATASOURCETYPE.YFINANCE
        self.data_source_type_fundamentals = None

    # If period is not None it will precede over date

    def set_date_parameters(self):
        self.period = None
        self.end_date = datetime.datetime.today()
        date_str = "01/01/2020"
        self.start_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        self.interval = Constants.INTERVAL.DAY

    def set_indicators(self):
        self.indicators = []

    def set_kpi(self):
        sortino = Sortino()
        self.kpis = [sortino]
