from Data.DataSource import DataSource

class YahooAPIDataSource(DataSource):


    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date



    def __init__(self, ticker):
        pass




    # all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "INTC"]
    def extract_historical_data(self):
        self.extract_data()

    def extract_data(self):
        pass
