from data.DataSource import DataSource
from stocks_model.StocksFactory import StocksFactory


from utilities.Constants import Constants
from stocks_model.Stock import Stock

import datetime


class StrategyManager:




    def __init__(self,
                 strategies,
                 tickers,
                 data_source_type,
                 start_date=datetime.date.today() - datetime.timedelta(1),
                 end_date=datetime.date.today(),
                 period=None,
                 interval=Constants.INTERVAL.DAY,
                 bulk=False
                 ):

        self.strategies = strategies

        self.tickers = tickers
        self.data_source_type = data_source_type
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.interval = interval

        self.bulk = bulk
        self.stocks = None




    def load_strategy(self):

        fundamentals = False
        historic = False

        for strategy in self.strategies:
            if strategy.fundamentals is True:
                fundamentals = True
            if strategy.historic is True:
                historic = True


            self.stocks = \
                StocksFactory.create_stocks(
                    tickers=self.tickers,
                    data_source_type=self.data_source_type,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    period=self.period,
                    interval=self.interval,
                    fundamentals=fundamentals,
                    historic=historic,
                    bulk=self.bulk

                )



