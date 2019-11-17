from fundamentals.Fundamentals import Fundamentals




class Stock:

    error = None

    fundamentals = None

    ticker = None



    def __init__(self, ticker):
        print("Stock {} created".format(ticker))
        self.ticker = ticker

    def get_fundamentals(self):
        self.fundamentals = Fundamentals(self.ticker)
        self.fundamentals.acquire_fundamentals()







