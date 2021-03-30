import abc
import pandas as pd
from utilities.Constants import Constants



class Indicator(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def __init__(self, params=None):

        if params is None:
            params = {}

        self.params = params


    @abc.abstractmethod
    def calculate(self, df, params):
        """function to calculate the indicator"""
        if df is None:
            print("Error: DF has not been set, there is no data to calculate the indicator. "
                  "Please verify the indicator constructor")
            raise IOError

        # Params can also be set in the constructor
        if params is not None:
            self.params = params

