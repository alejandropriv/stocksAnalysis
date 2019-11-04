from bs4 import BeautifulSoup
from fundamentals.FundamentalsParser import FundamentalsParser


class IncomeStatement:

    items = dict()

    elements = dict()


    def __init__(self, src):

        print("Scrapping the Income Statement")
        self.elements["BreakDown"] = ["Total Revenue",
                                      "Cost of Revenue",
                                      "Gross Profit",
                                      "Operating Income or Loss",
                                      "Interest Expense",
                                      "Total Other Income/Expenses Net",
                                      "Income Before Tax",
                                      "Income Tax Expense",
                                      "Income from Continuing Operations",
                                      "Net Income",
                                      "Net Income available to common shareholders"
                                      ]

        self.elements["Operating Expenses"] = ["Research Development",
                                               "Selling General and Administrative",
                                               "Total Operating Expenses"
                                               ]

        # self.elements["Reported_EPS"] = ["Basic","Diluted"]

        # self.elements["Weighted_average_shares_outstanding"] = ["Basic","Diluted"]


        parsed_html = BeautifulSoup(src.text, 'html.parser')
        self.set_income_statement_data(parsed_html)


    def set_income_statement_data(self, parsed_html):

        parser = FundamentalsParser()

        for category in self.elements:

            for search_string in self.elements[category]:

                item = parsed_html.find(text=search_string).parent

                self.items = parser.parse_data_model(item, "div")


        #############################################
        #############################################

        search_string = "Basic"

        basics_item = parsed_html.find_all(text=search_string)

        item = basics_item[0].parent

        self.items = parser.parse_data_model(item, "div")

        self.items["Reported EPS-Basic"] = self.items.pop("Basic")

        #############################################
        #############################################

        search_string = "Diluted"

        basics_item = parsed_html.find_all(text=search_string)

        item = basics_item[0].parent

        self.items = parser.parse_data_model(item, "div")

        self.items["Reported EPS-Basic"] = self.items.pop("Diluted")


        #############################################
        #############################################

        search_string = "Basic"

        basics_item = parsed_html.find_all(text=search_string)

        item = basics_item[1].parent

        self.items = parser.parse_data_model(item, "div")

        self.items["Weighted average shares outstanding-Basic"] = self.items.pop("Basic")



        #############################################
        #############################################

        search_string = "Diluted"

        basics_item = parsed_html.find_all(text=search_string)

        item = basics_item[0].parent

        self.items = parser.parse_data_model(item, "div")

        self.items["Weighted average shares outstanding-Diluted"] = self.items.pop("Diluted")



        print(self.items)



    def get_data(self):
        pass
