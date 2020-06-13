import abc


class KPI(metaclass=abc.ABCMeta):


        @abc.abstractmethod
        def __init__(self):
            self.ticker = None
            self.df = None
            self.value = None

        @abc.abstractmethod
        def set_input_data(self, df):
            if df is None:
                print("Error: data not found")
                raise IOError

            self.ticker = df.ticker
            self.value = None


        @abc.abstractmethod
        def calculate(self):
            """function to calculate the indicator"""
            if self.df is None:
                print("Error: DF has not been set Data not found to calculate the requested operation")
                raise IOError
