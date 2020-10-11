from strategy.Strategy import Strategy
from utilities.Constants import Constants
from indicators.RSI import RSI
from indicators.Slope import Slope
from data.DataSource import DATASOURCETYPE


import datetime



class StrategyIX(Strategy):

    name = "StrategyIX"

    def __init__(self):

        super().__init__()
        self.set_data_source_types()
        self.set_date_parameters()
        self.set_indicators()

    def set_data_source_types(self):
        self.data_source_type_historical = DATASOURCETYPE.YFINANCE
        self.data_source_type_fundamentals = None

    # If period is not None it will precede over date
    def set_date_parameters(self):
        self.period = None
        self.end_date = datetime.datetime.today()
        date_str = "11/07/2019"
        self.start_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        self.interval = Constants.INTERVAL.DAY

    def set_indicators(self):
        rsi = RSI(n=14)
        slope = Slope(n=5)


        self.indicators = [rsi, slope]
