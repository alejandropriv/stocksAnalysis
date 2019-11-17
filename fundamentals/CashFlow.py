from bs4 import BeautifulSoup
from utilities.RequestHandler import RequestHandler



class CashFlow:

    ticker = None
    data = {}

    def __init__(self, ticker):

        self.ticker = ticker

        print("\n\n--- Scrapping the Cash Flow - Ticker: "+self.ticker+" ---")
        self.webpage = "https://finance.yahoo.com/quote/"+self.ticker+"/cash-flow?p="+self.ticker

        request_handler = RequestHandler()
        src = request_handler.load_webpage(self.webpage)

        self.set_cash_flow(src.content)


    def set_cash_flow(self, page_content):

        soup = BeautifulSoup(page_content, 'html.parser')
        tabl = soup.find_all("div", {"class": "M(0) Mb(10px) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
        for t in tabl:
            rows = t.find_all("div", {"class": "rw-expnded"})
            for row in rows:
                self.data[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1:6]


    def get_data(self):
        return self.data

