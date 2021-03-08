# =============================================================================
# Measuring the performance of a buy and hold strategy - CAGR
# Author : Mayank Rasu (http://rasuquant.com/wp/)

# Please report bug/issues in the Q&A section
# =============================================================================

# Import necesary libraries
import yfinance as yf
import numpy as np
import datetime as dt
import pandas as pd
# Download historical data for required stocks
def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    print(df)
    df["daily_ret"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()
    n = len(df)/252
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    return CAGR


ticker = "TSLA"
SnP = yf.download(ticker,dt.datetime(2021, 3, 7)-dt.timedelta(1825), dt.datetime(2021, 3, 7))

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(CAGR(SnP))

