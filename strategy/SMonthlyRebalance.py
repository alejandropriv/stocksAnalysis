from strategy.Strategy import Strategy
from utilities.Constants import Constants
from kpi.Volatility import Volatility
from kpi.Sharpe import Sharpe
from kpi.CAGR import CAGR
from kpi.Calmar import Calmar
from kpi.MaxDrawdown import MaxDrawdown
from kpi.Sortino import Sortino
from data.DataSource import DATASOURCETYPE

from method.PortfolioRebalance import PortfolioRebalance

import datetime as dt


class SMonthlyRebalance(Strategy):

    name = "SMonthlyRebalance"

    def __init__(self):

        super().__init__()
        self.set_data_source_types()
        self.set_date_parameters()
        self.set_kpi()
        self.set_methods()



    def set_data_source_types(self):
        self.dst_historical = DATASOURCETYPE.YFINANCE
        self.dst_fundamentals = None

    # If period is not None it will precede over date
    def set_date_parameters(self):
        self.period = None
        self.end_date = dt.datetime.today()
        self.start_date = self.end_date - dt.timedelta(3650)
        self.interval = Constants.INTERVAL.MONTH

    def set_kpi(self):
        cagr = CAGR()
        calmar = Calmar()
        md = MaxDrawdown()
        sharpe = Sharpe()
        sortino = Sortino()
        volatility = Volatility()

        self.kpis = [cagr, calmar, md, sharpe, sortino, volatility]


    def set_methods(self):
        port_rebalance = PortfolioRebalance()
        self.methods = [port_rebalance]

