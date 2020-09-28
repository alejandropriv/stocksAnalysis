from strategy.Strategy import Strategy
from utilities.Constants import Constants
from indicators.ADX import ADX


import datetime



class StrategyVI(Strategy):


    def __init__(self):

        super().__init__()
        self.set_data_source_required_parameters()
        self.set_date_parameters()
        self.set_indicators()



    def set_data_source_required_parameters(self):
        self.historical = True
        self.fundamentals = True

    # If period is not None it will precede over date
    def set_date_parameters(self):
        self.period = None
        self.end_date = datetime.datetime.today()
        date_str = "11/07/2019"
        self.start_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        self.interval = Constants.INTERVAL.DAY

    def set_indicators(self):
        adx = ADX(n=14)

        self.indicators = [adx]
