# ./execution
# python3 Main.py
from PlotData import PlotData
from Stock import Stock
from Data.DataSource import DataSource


from StockPlot import StockPlot

class Main:

    apikey = "86VFFOKUNB1M9YQ8"

    fundamentals = True
    historical_data = True

    def __init__(self):

        self.tickers = ["FB", "TSLA", "", ""]# put validation on empty symbols

        stock = None

        for ticker in self.tickers:

            stock = Stock(ticker)
            stock.set_data_source(data_source_type=DataSource.DataSourceType.YAHOOFINANCIALS)


            if self.fundamentals:

                stock.get_fundamentals()
                print(stock.fundamentals.income_statement.get_data())
                print(stock.fundamentals.balance_sheet.get_data())
                print(stock.fundamentals.cash_flow.get_data())
                print(stock.fundamentals.statistics.get_data())


            if self.historical_data:

                stock.get_historical_data()












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



