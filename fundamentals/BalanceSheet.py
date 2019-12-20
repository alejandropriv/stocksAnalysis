from bs4 import BeautifulSoup
from utilities.RequestHandler import RequestHandler


class BalanceSheet:

    def __init__(self, ticker):

        self.ticker = ticker
        self.data = {}

        print("\n\n--- Scrapping the Balance Sheet - Ticker: "+self.ticker+" ---")

        self.webpage = "https://finance.yahoo.com/quote/" + self.ticker + "/balance-sheet?p=" + self.ticker

        request_handler = RequestHandler()
        src = request_handler.load_webpage(self.webpage)

        self.set_balance_sheet_data(src.content)



    def set_balance_sheet_data(self, page_content):

        # getting balance sheet data from yahoo finance for the given ticker

        soup = BeautifulSoup(page_content, 'html.parser')
        tabl = soup.find_all("div", {"class": "M(0) Mb(10px) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
        for t in tabl:
            rows = t.find_all("div", {"class": "rw-expnded"})
            for row in rows:
                self.data[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]


    def get_data(self):
        return self.data
