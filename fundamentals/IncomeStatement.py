from bs4 import BeautifulSoup


class IncomeStatement:

    data = {}

    def __init__(self, src):

        print("\n\n--- Scrapping the Income Statement ---")
        self.set_income_statement_data(src.content)


    def set_income_statement_data(self, page_content):

        soup = BeautifulSoup(page_content, 'html.parser')
        tabl = soup.find_all("div", {"class": "M(0) Mb(10px) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
        for t in tabl:
            rows = t.find_all("div", {"class": "rw-expnded"})
            for row in rows:
                self.data[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1:6]



    def get_data(self):
        return self.data


#
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
#
# tickers = ["AAPL", "MSFT"]  # list of tickers whose financial data needs to be extracted
# financial_dir = {}
#
# for ticker in tickers:
#     # getting balance sheet data from yahoo finance for the given ticker
#     temp_dir = {}
#     url = 'https://in.finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker
#     page = requests.get(url)
#     page_content = page.content
#     soup = BeautifulSoup(page_content, 'html.parser')
#     tabl = soup.find_all("div", {"class": "M(0) Mb(10px) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
#     for t in tabl:
#         rows = t.find_all("div", {"class": "rw-expnded"})
#         for row in rows:
#             temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]
#
#     # getting income statement data from yahoo finance for the given ticker
#     url = 'https://in.finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
#     page = requests.get(url)
#     page_content = page.content
#     soup = BeautifulSoup(page_content, 'html.parser')
#     tabl = soup.find_all("div", {"class": "M(0) Mb(10px) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
#     for t in tabl:
#         rows = t.find_all("div", {"class": "rw-expnded"})
#         for row in rows:
#             temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]
#
#     # getting cashflow statement data from yahoo finance for the given ticker
#     url = 'https://in.finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' + ticker
#     page = requests.get(url)
#     page_content = page.content
#     soup = BeautifulSoup(page_content, 'html.parser')
#     tabl = soup.find_all("div", {"class": "M(0) Mb(10px) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
#     for t in tabl:
#         rows = t.find_all("div", {"class": "rw-expnded"})
#         for row in rows:
#             temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]
#
#     # getting key statistics data from yahoo finance for the given ticker
#     url = 'https://in.finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' + ticker
#     page = requests.get(url)
#     page_content = page.content
#     soup = BeautifulSoup(page_content, 'html.parser')
#     tabl = soup.findAll("table", {"class": "W(100%) Bdcl(c) Mt(10px) "})
#     for t in tabl:
#         rows = t.find_all("tr")
#         for row in rows:
#             if len(row.get_text(separator='|').split("|")[0:2]) > 0:
#                 temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[-1]
#
#                 # combining all extracted information with the corresponding ticker
#     financial_dir[ticker] = temp_dir
#
#     print(financial_dir)
# # storing information in pandas dataframe
# combined_financials = pd.DataFrame(financial_dir)
# tickers = combined_financials.columns
# for ticker in tickers:
#     combined_financials = combined_financials[~combined_financials[ticker].str.contains("[a-z]").fillna(False)]