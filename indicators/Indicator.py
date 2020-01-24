import abc


class Indicator(metaclass=abc.ABCMeta):


        @abc.abstractmethod
        def __init__(self):
            self.ticker = None
            self.df_macd = None



        @abc.abstractmethod
        def set_input_data(self, df):
            if df is None:
                print("Error: data not found")
                raise IOError

            self.df_macd = df


            self.ticker = df.ticker


        @abc.abstractmethod
        def calculate(self):
            """function to calculate the indicator"""
            pass

        @abc.abstractmethod
        def plot(self, period=100, color="tab:green"):
            pass
