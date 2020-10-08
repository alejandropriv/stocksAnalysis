from stocks_model.StocksFactory import StocksFactory


class StrategyManager:


    def __init__(self,
                 strategies,
                 tickers,
                 data_source_type_historic=None,
                 data_source_type_fundamentals=None,
                 bulk=False):

        self.strategies = strategies

        self.tickers = tickers

        if data_source_type_historic is None and data_source_type_fundamentals is None:
            raise ValueError("Please define historic or fundamentals DataSource")

        if data_source_type_fundamentals is None:
            self.data_source_type_fundamentals = data_source_type_historic
        if data_source_type_historic is None:
            self.data_source_type_historic = data_source_type_fundamentals

        else:
            self.data_source_type_fundamentals = data_source_type_fundamentals
            self.data_source_type_historic = data_source_type_historic


        self.bulk = bulk
        self.stocks_per_strategy = {}

        self.load_strategy()



    def load_strategy(self):


        for strategy in self.strategies:

            self.stocks_per_strategy[strategy.name] = \
                StocksFactory.create_stocks(
                        tickers=self.tickers,
                        data_source_type_historic=self.data_source_type_historic,
                        data_source_type_fundamentals=self.data_source_type_fundamentals,
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

