import abc


class Indicator(metaclass=abc.ABCMeta):


        @abc.abstractmethod
        def __init__(self):
            self.ticker = None
            self.df = None


        @abc.abstractmethod
        def set_input_data(self, df):
            if df is None:
                print("Error: data not found")
                raise IOError

            self.ticker = df.ticker



        @abc.abstractmethod
        def calculate(self):
            """function to calculate the indicator"""
            if self.df is None:
                print("Error: data not found")
                raise IOError

        @abc.abstractmethod
        def plot(self, plotter=None, period=100, color="tab:green"):
            if plotter is None:
                print("Please Select the main stock first.")
                raise IOError
