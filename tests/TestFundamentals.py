import unittest

from strategy.test_strategies.StrategyXII import StrategyXII
from strategy.StrategyManager import StrategyManager
from data.AlphaAPIDataSource import AlphaAPIDataSource

from plotter.Plotter import Plotter



DEVELOPMENT = True

class TestBasics(unittest.TestCase):
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None


    def test_fundamentals(self):
        AlphaAPIDataSource._QA_API_KEY = True
        tickers = ["TSLA", "SNAP"]

        strategies = [StrategyXII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=True)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            pass
            #plt.show()



if __name__ == '__main__':
    unittest.main()
