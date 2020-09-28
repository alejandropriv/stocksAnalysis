from enum import Enum



from stocks_model.StocksFactory import StocksFactory
from strategy.test_strategies.StrategyI import StrategyI
from strategy.test_strategies.StrategyII import StrategyII
from strategy.test_strategies.StrategyIII import StrategyIII
from strategy.test_strategies.StrategyIV import StrategyIV
from strategy.test_strategies.StrategyV import StrategyV
from strategy.test_strategies.StrategyVI import StrategyVI
from strategy.test_strategies.StrategyXI import StrategyXI
from strategy.test_strategies.StrategyXII import StrategyXII



from strategy.test_strategies.StrategyX import StrategyX




class AV_STRATEGY(Enum):
    STRATEGYI = 1  # Show only the Stock plot
    STRATEGYII = 2  # Bollinger Bands
    STRATEGYIII = 3  # MACD
    STRATEGYIV = 4  # ATR
    STRATEGYV = 5  # RSI
    STRATEGYVI = 6  # ADX
    STRATEGYX = 10  # MACD_ATR
    STRATEGYXI = 11  # MACD_RSI
    STRATEGYXII = 12  # MACD_RSI_ATR_ADX_OBV_BB


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

        if strategy_type is AV_STRATEGY.STRATEGYI:
            return StrategyI()
        if strategy_type is AV_STRATEGY.STRATEGYII:
            return StrategyII()
        elif strategy_type is AV_STRATEGY.STRATEGYIII:
            return StrategyIII()
        elif strategy_type is AV_STRATEGY.STRATEGYIV:
            return StrategyIV()
        elif strategy_type is AV_STRATEGY.STRATEGYV:
            return StrategyV()
        elif strategy_type is AV_STRATEGY.STRATEGYVI:
            return StrategyVI()
        elif strategy_type is AV_STRATEGY.STRATEGYX:
            return StrategyX()
        elif strategy_type is AV_STRATEGY.STRATEGYXI:
            return StrategyXI()
        elif strategy_type is AV_STRATEGY.STRATEGYXII:
            return StrategyXII()




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

