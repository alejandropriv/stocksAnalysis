from bs4 import BeautifulSoup

class Statistics:

    data = {}

    def __init__(self, src):
        print("\n\n--Scrapping the Statistics---")

        self.set_statistics_data(src.content)



    def set_statistics_data(self, page_content):

        # getting key statistics data from yahoo finance for the given ticker
        soup = BeautifulSoup(page_content, 'html.parser')
        tabl = soup.find_all("table", {"class": "W(100%) Bdcl(c) Mt(10px)  Mb(10px)"})
        for t in tabl:
            rows = t.find_all("tr")
            for row in rows:
                if len(row.get_text(separator='|').split("|")[0:2]) > 0:
                    self.data[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[-1]



    def get_data(self):
        return self.data
