# =============================================================================
# Measuring the performance of a buy and hold strategy - Volatility
# Author : Mayank Rasu (http://rasuquant.com/wp/)

# Please report bug/issues in the Q&A section
# =============================================================================

# Import necesary libraries
import yfinance as yf
import numpy as np
import datetime as dt

# Download historical data for required stocks
def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)
    return vol


ticker = "TSLA"
SnP = yf.download(ticker,dt.datetime(2021, 3, 7)-dt.timedelta(1825), dt.datetime(2021, 3, 7))
print(volatility(SnP))