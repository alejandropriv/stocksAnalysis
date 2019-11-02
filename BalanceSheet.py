# ./execution
# python3 BalanceSheet.py

from bs4 import BeautifulSoup
class BalanceSheet:

    TotalRevenue = dict()
    parsedHtml = None
    items = None
    src = None


    def __init__(self, src):

        self.src = src
        self.parsedHtml = BeautifulSoup(self.src.text, 'lxml')
        self.items = self.parsedHtml.find_all("span")

        self.items = self.parsedHtml.find(text='Total Revenue').find_next('span').getText()

        print(self.items)

        #print(self.parsedHtml)
        #print(self.parsedHtml.prettify())

        self.set_data("TotalRevenue")


    def set_data(self, searchString):
        for item in self.items:
            print(item.getText())


    def get_data(self):
        pass






