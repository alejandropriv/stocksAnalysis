from bs4 import BeautifulSoup
from fundamentals.FundamentalsParser import FundamentalsParser


class BalanceSheet:
    items = None

    elements = None

    def __init__(self, src):
        print("Scrapping the Balance Sheet")

        self.items = dict()

        self.elements = dict()

        cash = ["Cash And Cash Equivalents",
                "Short Term Investments",
                "Total Cash"
                ]

        current_assets = [cash,
                          "Net Receivables",
                          "Inventory",
                          "Other Current Assets",
                          "Total Current Assets"
                          ]

        property_plant_equipment = ["Gross property, plant and equipment",
                                    "Accumulated Depreciation",
                                    "Net property, plant and equipment"
                                    ]

        non_current_assets = [
            property_plant_equipment,
            "Equity and other investments",
            "Goodwill",
            "Intangible Assets",
            "Other long-term assets",
            "Total non-current assets"
        ]


        self.elements["Assets"] = [
            current_assets,
            non_current_assets,
            "Total Assets"]

        current_liabilities = [
            "Total Revenue",
            "Accounts Payable",
            "Taxes payable",
            "Accrued liabilities",
            "Deferred revenues",
            "Other Current Liabilities",
            "Total Current Liabilities"
        ]

        non_current_liabilities = [
            "Long Term Debt",
            "Deferred taxes liabilities",
            "Deferred revenues",
            "Other long-term liabilities",
            "Total non-current liabilities"
        ]

        liabilities = [
            current_liabilities,
            non_current_liabilities,
            "Total Liabilities"]

        stockholders_equity = [
            "Common Stock",
            "Retained Earnings",
            "Accumulated other comprehensive income",
            "Total stockholders' equity"
        ]

        self.elements["Liabilities and stockholders equity"] = [
            liabilities,
            stockholders_equity
        ]


        parsed_html = BeautifulSoup(src.text, 'html.parser')
        self.set_balance_sheet_data(parsed_html)

    def set_balance_sheet_data(self, parsed_html):

        list_balance_sheet = self.traverse_data(self.elements)

        parser = FundamentalsParser()


        for search_string in list_balance_sheet:
            item = parsed_html.find(text=search_string).parent
            self.items = parser.parse_data_model(item, "div")

        print(self.items)






    def traverse_data(self, node):

        list_balance_sheet = []

        if isinstance(node, (list, tuple, dict)):

            for child in node:
                if isinstance(node, dict):
                    result = self.traverse_data(node[child])

                    if isinstance(result, (list, tuple)):
                        list_balance_sheet.extend(result)
                    else:
                        list_balance_sheet.append(result)

                else:

                    result = self.traverse_data(child)

                    if isinstance(result, (list, tuple)):
                        list_balance_sheet.extend(result)
                    else:
                        list_balance_sheet.append(result)

        else:

            return node

        return list_balance_sheet


    def get_data(self):
        pass
