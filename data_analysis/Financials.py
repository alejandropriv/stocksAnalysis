from enum import Enum

class Financials:

    def __init__(self):
        pass;

    @staticmethod
    def pct_change(input_df):

        return input_df.pct_change().fillna(0)
