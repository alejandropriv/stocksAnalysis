from enum import Enum



from stocks_model.StocksFactory import StocksFactory
from strategy.StrategyI import StrategyI
from strategy.StrategyMACD import StrategyMACD
from strategy.StrategyATR import StrategyATR
from strategy.StrategyMACDRSI import StrategyMACDRSI
from strategy.StrategyRSI import StrategyRSI
from strategy.StrategyBB import StrategyBB
from strategy.StrategyADX import StrategyADX

from strategy.StrategyX import StrategyX




class AV_STRATEGY(Enum):
    STRATEGYBB = 1
    STRATEGYMACD = 2
    STRATEGYATR = 3
    STRATEGYRSI = 4
    STRATEGYMACDRSI = 5
    STRATEGYADX = 6
    STRATEGYX = 10
    STRATEGYI = 11 # Show only the Stock plot




class StrategyManager:


    def __init__(self,
                 strategies,
                 tickers,
                 data_source_type,
                 bulk=False):

        self.strategies_type = strategies

        self.tickers = tickers
        self.data_source_type = data_source_type

        self.bulk = bulk
        self.stocks_per_strategy = {}

        self.load_strategy()


    @staticmethod
    def select_strategy(strategy_type):

        if strategy_type is AV_STRATEGY.STRATEGYBB:
            return StrategyBB()
        if strategy_type is AV_STRATEGY.STRATEGYI:
            return StrategyI()
        elif strategy_type is AV_STRATEGY.STRATEGYMACD:
            return StrategyMACD()
        elif strategy_type is AV_STRATEGY.STRATEGYATR:
            return StrategyATR()
        elif strategy_type is AV_STRATEGY.STRATEGYMACDRSI:
            return StrategyMACDRSI()
        elif strategy_type is AV_STRATEGY.STRATEGYRSI:
            return StrategyRSI()
        elif strategy_type is AV_STRATEGY.STRATEGYX:
            return StrategyX()
        elif strategy_type is AV_STRATEGY.STRATEGYADX:
            return StrategyADX()



        else:
            raise ValueError



    def load_strategy(self):


        for strategy_type in self.strategies_type:
            strategy = self.select_strategy(strategy_type)

            self.stocks_per_strategy[strategy_type.name] = \
                StocksFactory.create_stocks(
                        tickers=self.tickers,
                        data_source_type=self.data_source_type,
                        start_date=strategy.start_date,
                        end_date=strategy.end_date,
                        period=strategy.period,
                        interval=strategy.interval,
                        fundamentals=strategy.fundamentals,
                        historical=strategy.historical,
                        indicators=strategy.indicators,
                        bulk=self.bulk
                )

            self.run_strategies()


    def run_strategies(self):
        if not self.stocks_per_strategy: # Empty dictionary
            print("Error: Load Strategy first")
            raise ValueError


        self.report()





    def report(self):
        pass

