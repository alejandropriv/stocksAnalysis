from stocks_model.StocksFactory import StocksFactory


class StrategyManager:

    def __init__(self):
        pass


    @staticmethod
    def load_strategies(strategies, tickers, bulk=False):

        reports = {}
        results = {}
        stocks = {}
        for strategy in strategies:
            stocks[strategy.name] = \
                StocksFactory.create_stocks(
                    strategy=strategy,
                    tickers=tickers,
                    bulk=bulk
                )

            results[strategy.name] = StrategyManager.run_strategy(strategy, stocks[strategy.name])
            reports[strategy.name] = StrategyManager.run_report(strategy, results[strategy.name])

        return reports


    @staticmethod
    def run_strategy(strategy, stocks):
        results = {}
        if not strategy.methods:
            return stocks

        for method in strategy.methods:
            results[method.name] = method.execute(stocks)

        return strategy.methods

    @staticmethod
    def run_report(strategy, results):

        reports = {}
        if not strategy.reports:
            return results

        for report in strategy.reports:
            reports[report.name] = report.generate(results)

        return strategy.reports
