from strategy.Strategy import Strategy
from utilities.Constants import Constants

from data.DataSource import DATASOURCETYPE
from kpi.CAGR import CAGR
from kpi.Calmar import Calmar
from kpi.MaxDrawdown import MaxDrawdown
from kpi.Sharpe import Sharpe
from kpi.Sortino import Sortino
from kpi.Volatility import Volatility

from reports.BasicReport import BasicReport

import datetime as dt


class StrategyXX(Strategy):
    name = "StrategyXX"

    def __init__(self):
        super().__init__()
        self.set_data_source_types()
        self.set_date_parameters()
        self.set_indicators()
        self.set_kpi()
        self.set_report()

    def set_data_source_types(self):
        self.dst_historical = DATASOURCETYPE.YFINANCE
        self.dst_fundamentals = None

    # If period is not None it will precede over date

    def set_date_parameters(self):
        self.period = None
        self.end_date = dt.datetime(2021, 3, 7)
        # date_str = "01/01/2020"
        self.start_date = self.end_date-dt.timedelta(1825)
        self.interval = Constants.INTERVAL.DAY

    def set_indicators(self):
        self.indicators = []

    def set_kpi(self):
        params_cagr = {'period': self.interval}
        cagr = CAGR(params_cagr)

        params_calmar = {'period': self.interval}
        calmar = Calmar(params_calmar)

        md = MaxDrawdown()

        params_sharpe = {'rf': 0.0144, 'period': self.interval}
        sharpe = Sharpe(params_sharpe)

        params_sortino = {'rf': 0.0144, 'period': self.interval}
        sortino = Sortino(params_sortino)

        params_volatility = {'negative': False, 'period': self.interval}
        volatility = Volatility(params_volatility)

        self.kpis = [cagr, calmar, md, sharpe, sortino, volatility]

    def set_report(self):
        report = BasicReport()
        self.reports = [report]
