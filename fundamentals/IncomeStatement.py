# ./execution
# python3 IncomeStatement.py

from bs4 import BeautifulSoup
import re
import sys


class IncomeStatement:
    parsedHtml = None
    items = dict()
    src = None

    def __init__(self, src):

        self.src = src
        self.parsedHtml = BeautifulSoup(self.src.text, 'html.parser')

        # In this run Basic and diluted are filled with Bogus data, a run after will fix values for this keys
        search_string = "Total Revenue"

        item = self.parsedHtml.find(text=search_string).parent

        self.set_data_model(item, "EBITDA", "span")

        #############################################
        #############################################

        search_string = "Interest Expense"

        item = self.parsedHtml.find(text=search_string).parent

        self.set_data_model(item, "Interest Expense", "div")

        #############################################
        #############################################

        search_string = "Total Other Income.Expenses Net"

        item = self.parsedHtml.find(text=re.compile(search_string)).parent

        self.set_data_model(item, "Total Other Income", "div")

        #############################################
        #############################################

        search_string = "Basic"

        item = self.parsedHtml.find(text=search_string).parent.parent

        self.set_data_model(item, "Basic", "div")

        self.items["Reported EPS-Basic"] = self.items.pop("Basic")

        #############################################
        #############################################

        search_string = "Diluted"

        item = self.parsedHtml.find(text=search_string).parent.parent

        self.set_data_model(item, "Diluted", "div")

        self.items["Reported EPS-Diluted"] = self.items.pop("Diluted")

        #############################################
        #############################################

        search_string = "Basic"

        item = self.parsedHtml.find_all(text=search_string)[1].parent.parent

        self.set_data_model(item, "Basic", "div")

        self.items["Weighted average shares outstanding-Basic"] = self.items.pop("Basic")

        #############################################
        #############################################

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
                        if len(value) >= 0:
                            break

                        else:
                            item = item.find_next(html_tag)

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

    def get_data(self):
        pass
