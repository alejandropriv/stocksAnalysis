import pprint


class BasicReport:

    def __init__(self):
        pass

    @staticmethod
    def print(data):
        pp = pprint.PrettyPrinter(indent=4)
        for stock in data:
            pp.pprint(stock)
