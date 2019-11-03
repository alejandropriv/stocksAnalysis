# ./execution
# python3 BalanceSheet.py

from bs4 import BeautifulSoup
import re
import sys


class BalanceSheet:

    TotalRevenue = dict()
    parsedHtml = None
    items = dict()
    src = None


    def __init__(self, src):

        self.src = src
        self.parsedHtml = BeautifulSoup(self.src.text, 'html.parser')

        #print(self.parsedHtml.prettify())

        # In this run Basic and diluted are filled with Bogus data, a run after will fix values for this keys
        search_string = "Total Revenue"

        item = self.parsedHtml.find(text=search_string).parent

        self.set_data_model(item, "EBITDA", "span")

        print(self.items)


        search_string = "Interest Expense"

        item = self.parsedHtml.find(text=search_string).parent

        self.set_data_model(item, "Interest Expense", "div")

        print(self.items)



        search_string = "Total Other Income\/Expenses Net"

        item = self.parsedHtml.find(text=re.compile(search_string)).parent

        self.set_data_model(item, "Total Other Income", "div")

        print(self.items)


        search_string = "Basic"

        item = self.parsedHtml.find(text=search_string).parent.parent

        self.set_data_model(item, "Basic", "div")

        self.items["Reported EPS-Basic"] = self.items.pop("Basic")

        print(self.items)


        search_string = "Diluted"

        item = self.parsedHtml.find(text=search_string).parent.parent

        self.set_data_model(item, "Diluted", "div")

        self.items["Reported EPS-Diluted"] = self.items.pop("Diluted")


        print(self.items)





        search_string = "Basic"

        item = self.parsedHtml.find_all(text=search_string)[1].parent.parent

        self.set_data_model(item, "Basic", "div")

        self.items["Weighted average shares outstanding-Basic"] = self.items.pop("Basic")


        print(self.items)

        search_string = "Diluted"

        item = self.parsedHtml.find_all(text=search_string)[1].parent.parent

        self.set_data_model(item, "Diluted", "div")

        self.items["Weighted average shares outstanding-Diluted"] = self.items.pop("Diluted")

        print(self.items)





    def set_data_model(self, search_item, stop_string, html_tag):

            item = search_item

            values = []

            while True:
                try:

                    item = item.find_next(html_tag)

                    while True:
                        value = item.getText().replace(',', '')

                        if len(value) >= 1:
                            if len(value) == 1 and value == "-":
                                value = "-"
                                break

                            elif len(value) > 1:
                                break

                        else:
                            item = item.find_next(html_tag)

                    if value != "-":
                        m = re.search("(^[- ]?\\d+$|^\\s*$)", value)
                        m2 = re.search("(^[- ]?\\d+\\.\\d+$)", value)

                        if m is not None or m2 is not None:
                            values.append(float(value))

                        else:
                            self.items[search_item.get_text()] = values

                            if stop_string not in search_item.get_text():
                                self.set_data_model(item, stop_string, html_tag)

                            break

                    else:
                        values.append(value)


                except Exception as e:
                    exc_info = sys.exc_info()
                    print("Unexpected error:", exc_info, e)
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






