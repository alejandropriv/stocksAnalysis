# ./execution
# python3 BalanceSheet.py

from bs4 import BeautifulSoup
import re


class BalanceSheet:

    TotalRevenue = dict()
    parsedHtml = None
    items = dict()
    src = None


    def __init__(self, src):

        self.src = src
        self.parsedHtml = BeautifulSoup(self.src.text, 'html.parser')

        print(self.parsedHtml.prettify())

        #self.set_data("Total Revenue", "Weighted average shares outstanding", "span")
        #self.set_data("Income Before Tax", "Weighted average shares outstanding", "span")
        self.set_data("Total Other Income/Expenses Net", "Weighted average shares outstanding", "span")
        #self.set_data("Total Other Income", "Weighted average shares outstanding", "span")

        print(self.items)



    def set_data(self, search_string, stop_string, html_tag):


        search_string = search_string.replace("/", ".")
        print("Search Str: %s" % search_string)

        item = self.parsedHtml.find(text=re.compile(search_string))


        values = []

        while True:
            try:
                print("ITEM: "+item)
                item = item.find_next(html_tag)

                value = item.getText().replace(',', '')

                m = re.search("([^0-9,]+)", value)

                if m is None:

                    print(float(value))
                    values.append(value)

                else:
                    self.items[search_string] = values

                    if search_string != stop_string:
                        search_string = value
                        self.set_data(search_string, stop_string, html_tag)

                    break


            except Exception as e:
                print("Unexpected error:", e)
                break








        # ttm = item.find_next(html_tag)
        # ttm_1 = ttm.find_next(html_tag)
        # ttm_2 = ttm_1.find_next(html_tag)
        # ttm_3 = ttm_2.find_next(html_tag)
        # ttm_4 = ttm_3.find_next(html_tag)
        #
        # self.items["ttm"] = ttm.getText()
        # self.items["ttm_1"] = ttm_1.getText()
        # self.items["ttm_2"] = ttm_2.getText()
        # self.items["ttm_3"] = ttm_3.getText()
        # self.items["ttm_4"] = ttm_4.getText()



    def get_data(self):
        pass






