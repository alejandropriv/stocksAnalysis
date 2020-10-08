import unittest

from stocks_model.Stock import Stock
from strategy.test_strategies.StrategyXI import StrategyXI
from strategy.StrategyManager import StrategyManager
from data.DataSource import DATASOURCETYPE

from plotter.Plotter import Plotter


import pprint
import datetime



DEVELOPMENT = True

class TestBasics(unittest.TestCase):
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None


    def test_fundamentals_OLD(self):

        self.tickers = ["TSLA"]  # , "TSLA", "UBER"]


        self.stock = Stock(self.tickers)

        if self.fundamentals:
            self.stock.get_fundamentals()

            pp = pprint.PrettyPrinter(indent=4)

            for ticker, data in self.stock.fundamentals.items():
                print("--------- TICKER: {} ----------------".format(ticker))
                print("--------- INCOME STATEMENT: {} ----------------".format(ticker))
                pp.pprint(data.income_statement.get_data())

                print("--------- BALANCE SHEET: {} ----------------".format(ticker))
                pp.pprint(data.balance_sheet.get_data())

                print("--------- CASH FLOW: {} ----------------".format(ticker))
                pp.pprint(data.cash_flow.get_data())


    def get_historical_data(self):
        if self.historical_data:
            self.stock.get_historical_data()


    def test_fundamentals_(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [StrategyXI()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type_historic=DATASOURCETYPE.YFINANCE,
                bulk=True
            )

        # stocks_per_strategy = manager.stocks_per_strategy
        #
        #
        # print("Analysis has been run")
        #
        #
        # test_date = "14/07/2020"
        # test_df = stocks_per_strategy[StrategyXI.name][0].price_info
        # ticker = "TSLA"
        # values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        # i = 0
        # for metric in ["High", "Low", "Open", "Close", "Volume"]:
        #     value = TestIndicators.truncate(
        #         test_df[ticker][metric].loc[
        #             test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
        #             ].iloc[0])
        #     assert value == TestIndicators.truncate(values[i]), value
        #     i += 1


    def test_fundamentals(self):
        tickers = ["TSLA", "SNAP"]  # , "SPY", "CCL"

        strategies = [AV_STRATEGY.STRATEGYCI]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                data_source_type_historic=DATASOURCETYPE.YFINANCE
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)
                plotter = Plotter(period=1000)
                plotter.plot_stock(stock, collapse_indicators=False)

        print("Analysis has been run")

        if DEVELOPMENT == True:
            plt.show()

        test_date = "14/07/2020"
        test_df = stocks_per_strategy[AV_STRATEGY.STRATEGYCI.name][0].price_info
        ticker = "TSLA"
        values = [318.0, 286.2, 311.2, 303.359, 117090500.0]

        i = 0
        for metric in ["High", "Low", "Open", "Close", "Volume"]:
            value = TestIndicators.truncate(
                test_df[ticker][metric].loc[
                    test_df[ticker][metric].index == datetime.datetime.strptime(test_date, "%d/%m/%Y")
                    ].iloc[0])
            assert value == TestIndicators.truncate(values[i]), value
            i += 1


if __name__ == '__main__':
    unittest.main()
