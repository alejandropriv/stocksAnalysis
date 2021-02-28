from strategy.Strategy import Strategy
from utilities.Constants import Constants

from data.DataSource import DATASOURCETYPE
from kpi.CAGR import CAGR
from kpi.Calmar import Calmar
from kpi.MaxDrawdown import MaxDrawdown

from reports.BasicReport import BasicReport

import datetime


class StrategyXX(Strategy):
    name = "StrategyXX"

    def __init__(self):
        super().__init__()
        self.set_data_source_types()
        self.set_date_parameters()
        self.set_indicators()
        self.set_kpi()

    def set_data_source_types(self):
        self.dst_historical = DATASOURCETYPE.YFINANCE
        self.dst_fundamentals = None

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
        cagr = CAGR()
        calmar = Calmar()
        md = MaxDrawdown()
        calmar.negative = False
        self.kpis = [cagr, calmar, md]

    def set_report(self):
        report = BasicReport()
        self.reports = [report]
