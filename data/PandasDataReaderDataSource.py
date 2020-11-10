# from data.DataSource import DataSource
# import pandas as pd
# from pandas_datareader import data as pdr
# from utilities.Constants import Constants
#
# import sys
#
# import datetime
#
#
# class PandasDataReaderDataSource(DataSource):
#
#     def __init__(self):
#         super().__init__()
#         self.prices = pd.DataFrame()
#
#     def extract_historical_data(self,
#                                 tickers,
#                                 start_date=datetime.date.today() - datetime.timedelta(1),
#                                 end_date=(datetime.date.today()),
#                                 period=None,
#                                 interval=Constants.INTERVAL.DAY):
#
#
#
#         self.tickers = tickers
#         self.tickers_str = self.get_tickers_str()
#
#         self.start_date = start_date
#         self.end_date = end_date
#         self.period = period
#         self.interval = interval
#         self.interval_str = interval.name
#
#         if self.period is not None:
#             self.start_date = None
#             self.end_date = None
#
#         self.validate_parameters()
#
#         self.extract_data()
#
#     def validate_parameters(self):
#         if self.interval is Constants.INTERVAL.MINUTE and \
#                 self.interval is Constants.INTERVAL.MINUTE2 and \
#                 self.interval is Constants.INTERVAL.MINUTE5 and \
#                 self.interval is Constants.INTERVAL.MINUTE15 and \
#                 self.interval is Constants.INTERVAL.MINUTE30 and \
#                 self.interval is Constants.INTERVAL.MINUTE60 and \
#                 self.interval is Constants.INTERVAL.MINUTE90 and \
#                 self.interval is Constants.INTERVAL.HOUR:
#
#             print("Interval is no available for this Data-Source")
#             raise AttributeError
#
#     def get_tickers_str(self):
#
#         tickers_str = ""
#         for ticker in self.tickers:
#             tickers_str = self.tickers_str + " " + ticker;
#
#         return tickers_str
#
#     def extract_data(self):
#
#         interval = ""
#         if self.time_series == Constants.INTERVAL.DAY:
#             interval = 'd'
#
#         elif self.time_series == Constants.INTERVAL.WEEK:
#             interval = 'w'
#
#         elif self.time_series == Constants.INTERVAL.MONTH:
#             interval = 'm'
#
#         # extracting stock data (historical close price) for the stocks identified
#         for ticker in self.tickers:
#
#             attempt = 0
#
#             high_key = Constants.get_high_key(ticker)
#             low_key = Constants.get_low_key(ticker)
#             open_key = Constants.get_open_key(ticker)
#             close_key = Constants.get_close_key(ticker)
#             adj_close_key = Constants.get_adj_close_key(ticker)
#             volume_key = Constants.get_volume_key(ticker)
#
#             while attempt <= 5:
#                 print("-------------------------------------")
#                 print("Ticker: {0} - attempt number:{1} ".format(ticker, attempt))
#                 print("-------------------------------------")
#
#                 try:
#                     temp = pdr.get_data_yahoo(ticker, self.start_date, self.end_date, interval=interval)
#
#                     print("Ticker: {0} - data received! ".format(ticker))
#
#                     temp.dropna(inplace=True)
#

#                     if self.data_columns[0] == "all":
#                         self.prices[high_key] = temp["High"]
#                         self.prices[low_key] = temp["Low"]
#                         self.prices[open_key] = temp["Open"]
#                         self.prices[close_key] = temp["Close"]
#                         self.prices[adj_close_key] = temp["Adj Close"]
#                         self.prices[volume_key] = temp["Volume"]
#
#                     break
#
#
#                 except Exception as why:
#                     print("Unexpected error:{}, Why:{}".format(sys.exc_info(), why))
#                     print(ticker, " :failed to fetch data...retrying")
#                     attempt += 1
#
#                     continue
#
#         self.prices.bfill(axis=0, inplace=True)
