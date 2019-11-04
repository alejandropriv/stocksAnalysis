import re
import sys

class FundamentalsParser:

    items = dict()

    def __init__(self):
        print("NewFundamental parser")


    def parse_data_model(self, search_item, html_tag, stop_string=None):


        item = search_item

        values = []

        while True:
            try:

                item = item.find_next(html_tag)

                while True:
                    value = item.getText().replace(',', '')

                    if len(value) > 0:
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

                        if stop_string is not None and stop_string not in search_item.get_text():
                            self.parse_data_model(item, html_tag, stop_string)

                        break

                else:
                    values.append(value)


            except Exception as e:
                exc_info = sys.exc_info()
                print("Unexpected error:", exc_info, e)
                print("Current Items at exception: " + str(self.items))
                break


        return self.items
