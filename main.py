# ./execution
# python3 Main.py
from PlotData import PlotData
from Stock import Stock
from scrapper.Scrapper import Scrapper

class Main:

    apikey = "86VFFOKUNB1M9YQ8"

    def __init__(self):

        self.tickers = ["FB", "TSLA"]

        scrapper = Scrapper(self.tickers)
        scrapper.get_fundamentals()




        self.owned_stocks = []


        PlotData.set_interactive_mode(True)

        i = len(self.tickers)

        for symbol_str in self.tickers:

            i -= 1
            if i == 0:
                PlotData.set_interactive_mode(False)

            stock = Stock(self.apikey, symbol_str)
            stock.retrieve_daily_data(True)
            stock.print_metadata()
            self.owned_stocks.append(stock)





main = Main()



