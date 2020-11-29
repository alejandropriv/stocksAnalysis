import unittest

from strategy.test_strategies.StrategyXII import StrategyXII
from strategy.StrategyManager import StrategyManager
from data.AlphaAPIDataSource import AlphaAPIDataSource



DEVELOPMENT = True

class TestBasics(unittest.TestCase):
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None




    def test_magic_formula_bulk(self): # Magic Formula only makes sense in Bulk mode
        AlphaAPIDataSource._QA_API_KEY = True
        tickers = ["TSLA", "SNAP"]

        strategies = [StrategyXII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)


        print("Fundamentals has been queried")

if __name__ == '__main__':
    unittest.main()
