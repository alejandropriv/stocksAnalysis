import abc
import pandas as pd

class ValueInvestmentMetric(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def __init__(self):
        self.tickers = None

        self.overview = None
        self.balance_sheet = None
        self.income_statement = None
        self.cashflow = None
        self.metric_df = pd.DataFrame()


    @abc.abstractmethod
    def set_input_data(self, fundamentals):
        if fundamentals is None:
            raise ValueError("Error: data not found")

        # TODO: create function get_ticker to get ticker and validate data

        self.tickers = fundamentals_df.columns.levels[0]


    @abc.abstractmethod
    def calculate(self):
        """function to calculate the indicator"""
        if self.overview is None and\
                self.balance_sheet is None and\
                self.income_statement is None and \
                self.cashflow is None:

            print("Error: Data has not been set, there is no data to calculate the metric. "
                  "Please verify the metric constructor")
            raise IOError


