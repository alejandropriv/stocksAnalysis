from enum import Enum
import datetime



from stocks_model.StocksFactory import StocksFactory
from strategy.StrategyI import StrategyI

from utilities.Constants import Constants


class AV_STRATEGY(Enum):
    STRATEGYI = 1
#    PANDASDATAREADER = 2


class StrategyManager:


    def __init__(self,
                 strategies,
                 tickers,
                 data_source_type,
                 bulk=False
                 ):

        self.strategies_type = strategies

        self.tickers = tickers
        self.data_source_type = data_source_type

        self.bulk = bulk
        self.stocks_per_strategy = {}
        self.load_strategy()


    def select_strategy(self, strategy_type):
        if strategy_type is AV_STRATEGY.STRATEGYI:
            return StrategyI()

    def load_strategy(self):


        for strategy_type in self.strategies_type:
            strategy = self.select_strategy(strategy_type)


            self.stocks_per_strategy[strategy_type.value] = \
                StocksFactory.create_stocks(
                        tickers=self.tickers,
                        data_source_type=self.data_source_type,
                        start_date=strategy.start_date,
                        end_date=strategy.end_date,
                        period=strategy.period,
                        interval=strategy.interval,
                        fundamentals=strategy.fundamentals,
                        historical=strategy.historical,
                        bulk=self.bulk
                )



