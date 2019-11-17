# ./execution
# python3 Main.py
from PlotData import PlotData
from Stock import Stock

from StockPlot import StockPlot

class Main:

    apikey = "86VFFOKUNB1M9YQ8"

    run_fundamentals = True

    def __init__(self):

        self.tickers = ["FB", "TSLA"]

        for ticker in self.tickers:

            if self.run_fundamentals:

                stock = Stock(ticker)
                stock.get_fundamentals()
                print(stock.fundamentals.income_statement.get_data())
                print(stock.fundamentals.balance_sheet.get_data())
                print(stock.fundamentals.cash_flow.get_data())
                print(stock.fundamentals.statistics.get_data())













        PlotData.set_interactive_mode(True)

        i = len(self.tickers)

        for symbol_str in self.tickers:

            i -= 1
            if i == 0:
                PlotData.set_interactive_mode(False)

            stock_plot = StockPlot(self.apikey, symbol_str)
            stock_plot.retrieve_daily_data(True)
            stock_plot.print_metadata()
            stocks = []

            stocks.append(stock_plot)





main = Main()



