from enum import Enum




class DailyReturn():

    class DATASOURCETYPE(Enum):

        YAHOOFINANCIALS = 1
        YAHOOAPI = 2
        ALPHAAPI = 3


    period = None


    prices = None
    daily_return = None



    def __init__(self, prices, period):

        self.prices = prices
        self.period = period




    def get_statistical_data(self):
        # Handling NaN Values
        self.prices.fillna(method='bfill', axis=0,
                           inplace=True)  # Replaces NaN values with the next valid value along the column

        self.prices.dropna(how='any', axis=0, inplace=True)  # Deletes any row where NaN value exists

        # Mean, Median, Standard Deviation, daily return
        self.prices.mean()  # prints mean stock price for each stock
        self.prices.median()  # prints median stock price for each stock
        self.prices.std()  # prints standard deviation of stock price for each stock

        self.daily_return = self.prices.pct_change()  # Creates dataframe with daily return for each stock

        self.daily_return.mean()  # prints mean daily return for each stock
        self.daily_return.std()  # prints standard deviation of daily returns for each stock

        # Rolling mean and standard deviation
        self.daily_return.rolling(window=self.period).mean()  # simple moving average
        self.daily_return.rolling(window=self.period).std()

        self.daily_return.ewm(span=self.period, min_periods=self.period).mean()  # exponential moving average
        self.daily_return.ewm(span=self.period, min_periods=self.period).std()


