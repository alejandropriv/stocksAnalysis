from stocks_model.StocksFactory import StocksFactory


class StrategyManager:


    def __init__(self,
                 strategies,
                 tickers,
                 bulk=False):

        self.strategies = strategies

        self.tickers = tickers


        self.bulk = bulk
        self.stocks_per_strategy = {}

        self.load_strategy()



    def load_strategy(self):


        for strategy in self.strategies:

            self.stocks_per_strategy[strategy.name] = \
                StocksFactory.create_stocks(
                    strategy=strategy,
                    tickers=self.tickers,
                    bulk=self.bulk
                )

            self.run_strategies()


    def run_strategies(self):
        if not self.stocks_per_strategy:  # Empty dictionary
            print("Error: Load Strategy first")
            raise ValueError

        self.report()


    def report(self):
        pass

