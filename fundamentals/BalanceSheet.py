from bs4 import BeautifulSoup
import pandas as pd

from utilities.RequestHandler import RequestHandler


class BalanceSheet:

    def __init__(self, ticker):

        self.ticker = ticker
        self.datadf = {}
        self.datapydf = {}
        self.datapy2df = {}

        self.filter = ["Cash And Cash Equivalents", "Short Term Investments"]


        print("\n\n--- Scrapping the Balance Sheet - Ticker: "+self.ticker+" ---")

        self.webpage = "https://finance.yahoo.com/quote/" + self.ticker + "/balance-sheet?p=" + self.ticker

        request_handler = RequestHandler()
        src = request_handler.load_webpage(self.webpage)

        self.set_balance_sheet_data(src.content)




    def set_balance_sheet_data(self, page_content):

        data = {}
        datapy = {}
        datapy2 = {}
        # getting balance sheet data from yahoo finance for the given ticker

        soup = BeautifulSoup(page_content, 'html.parser')
        #    tabl = soup.find_all("table", {"class" : "Lh(1.7) W(100%) M(0)"})

        tabl = soup.find_all("div", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
        #for t in tabl:
        #print(t)
        #rows = soup.find_all("div", {"class": "rw-expnded"})

        t = soup.find_all("div", {"id": "mrt-node-Col1-1-Financials"})
        for ro in t:
            print(ro)

            #rows = soup.find_all("div", {"data-test": "fin-row"})
            rows = ro.find_all("div", {"class": "rw-expnded"})

            print(rows)

            rows2 = ro.find_all("div", {"data-test": "fin-row"})

            #rows = soup.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
            for row in rows:
                print (row)
                indexName = row.get_text(separator='|').split("|")[0]

                if True: #indexName in self.filter:
                    data[indexName] = row.get_text(separator='|').split("|")[1]
                    datapy[indexName] = row.get_text(separator='|').split("|")[2]
                    datapy2[indexName] = row.get_text(separator='|').split("|")[3]


        self.datadf = pd.DataFrame.from_dict(data, orient='index')
        self.datapydf = pd.DataFrame.from_dict(datapy, orient='index')
        self.datapy2df = pd.DataFrame.from_dict(datapy2, orient='index')



        print("")


    def get_data(self):
        return self.datadf
