from utilities.Constants import Constants
from method.Method import Method
import pandas as pd


class PortfolioRebalance(Method):
    def __init__(self, df=None):
        super().__init__()

        if df is not None:
            self.set_input_data(df)

    def set_input_data(self, df):
        self.set_input_df(df)

        prices_temp = pd.DataFrame()

        df_list = []
        for ticker in self.tickers:
            df_list.append(
                pd.concat(
                    [df[ticker].loc[:, [self.prices_key]], prices_temp],
                    axis=1,
                    keys=[ticker]
                )
            )

        df_pr = pd.concat(
            df_list,
            axis=1
        )

        self.df = df_pr.copy()


    def back_test(self):

        """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""
        super().calculate()
        ################################Backtesting####################################

        df_result = []
        ohlc_mon = {}  # directory with ohlc value for each stock
        ohlc_dict = copy.deepcopy(ohlc_mon)
        return_df = pd.DataFrame()

        for ticker in self.tickers:
            df_data = self.df[ticker].copy()
            print("calculating monthly return for ", ticker)
            ohlc_dict[ticker]["mon_ret"] = ohlc_dict[ticker]["Adj Close"].pct_change()
            return_df[ticker] = ohlc_dict[ticker]["mon_ret"]



    # function to calculate portfolio return iteratively
    def pflio(DF, m, x):
        """Returns cumulative portfolio return
        DF = dataframe with monthly return info for all stocks
        m = number of stock in the portfolio
        x = number of underperforming stocks to be removed from portfolio monthly"""
        df = DF.copy()
        portfolio = []
        monthly_ret = [0]
        for i in range(len(df)):
            if len(portfolio) > 0:
                monthly_ret.append(df[portfolio].iloc[i, :].mean())
                bad_stocks = df[portfolio].iloc[i, :].sort_values(ascending=True)[:x].index.values.tolist()
                portfolio = [t for t in portfolio if t not in bad_stocks]
            fill = m - len(portfolio)
            new_picks = df.iloc[i, :].sort_values(ascending=False)[:fill].index.values.tolist()
            portfolio = portfolio + new_picks
            print(portfolio)
        monthly_ret_df = pd.DataFrame(np.array(monthly_ret), columns=["mon_ret"])
        return monthly_ret_df

    # calculating overall strategy's KPIs
        CAGR(pflio(return_df, 6, 3))
        sharpe(pflio(return_df, 6, 3), 0.025)
        max_dd(pflio(return_df, 6, 3))

        # calculating KPIs for Index buy and hold strategy over the same period
        DJI = yf.download("^DJI", dt.date.today() - dt.timedelta(3650), dt.date.today(), interval='1mo')
        DJI["mon_ret"] = DJI["Adj Close"].pct_change().fillna(0)
        CAGR(DJI)
        sharpe(DJI, 0.025)
        max_dd(DJI)

        # visualization
        fig, ax = plt.subplots()
        plt.plot((1 + pflio(return_df, 6, 3)).cumprod())
        plt.plot((1 + DJI["mon_ret"].reset_index(drop=True)).cumprod())
        plt.title("Index Return vs Strategy Return")
        plt.ylabel("cumulative return")
        plt.xlabel("months")
        ax.legend(["Strategy Return", "Index Return"])
        plt.show()
