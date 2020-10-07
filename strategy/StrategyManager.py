from stocks_model.StocksFactory import StocksFactory


class StrategyManager:


    def __init__(self,
                 strategies,
                 tickers,
                 data_source_type,
                 bulk=False):

        self.strategies = strategies

        self.tickers = tickers
        self.data_source_type = data_source_type

        self.bulk = bulk
        self.stocks_per_strategy = {}

        self.load_strategy()



    def load_strategy(self):


        for strategy in self.strategies:

            self.stocks_per_strategy[strategy.name] = \
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
        if not self.stocks_per_strategy:  # Empty dictionary
            print("Error: Load Strategy first")
            raise ValueError

        self.report()


    def report(self):
        pass

