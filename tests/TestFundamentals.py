import unittest

from strategy.test_strategies.StrategyXII import StrategyXII
from strategy.StrategyManager import StrategyManager
from data.AlphaAPIDataSource import AlphaAPIDataSource



DEVELOPMENT = True

class TestBasics(unittest.TestCase):
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None

    def test_magic_formula(self):
        AlphaAPIDataSource._QA_API_KEY = True
        tickers = ["ATVI", "GOOGL", "GOOG", "T", "CHTR", "CMCSA", "DISCA", "DISCK", "DISH", "EA", "FB", "FOXA", "FOX", "IPG", "LYV", "LUMN", "NFLX", "NWSA", "NWS", "OMC", "TMUS", "TTWO", "TWTR", "VZ", "VIAC", "DIS", "AAP", "AMZN", "APTV", "AZO", "BBY", "BKNG", "BWA", "KMX", "CCL", "CMG", "DHI", "DRI", "DG", "DLTR", "DPZ", "EBAY", "ETSY", "EXPE", "F", "GPS", "GRMN", "GM", "GPC", "HBI", "HAS", "HLT", "HD", "LB", "LVS", "LEG", "LEN", "LKQ", "LOW", "MAR", "MCD", "MGM", "MHK", "NWL", "NKE", "NCLH", "NVR", "ORLY", "POOL", "PHM", "PVH", "RL", "ROST", "RCL", "SBUX", "TPR", "TGT", "TSLA", "TIF", "TJX", "TSCO", "ULTA", "UAA", "UA", "VFC", "WHR", "WYNN", "YUM", "MO", "ADM", "BF.B", "CPB", "CHD", "CLX", "KO", "CL", "CAG", "STZ", "COST", "EL", "GIS", "HSY", "HRL", "SJM", "K", "KMB", "KHC", "KR", "LW", "MKC", "TAP", "MDLZ", "MNST", "PEP", "PM", "PG", "SYY", "TSN", "WMT", "WBA", "APA", "BKR", "COG", "CVX", "CXO", "COP", "DVN", "FANG", "EOG", "XOM", "HAL", "HES", "HFC", "KMI", "MRO", "MPC", "NOV", "OXY", "OKE", "PSX", "PXD", "SLB", "FTI", "VLO", "WMB", "ABT", "ABBV", "ABMD", "A", "ALXN", "ALGN", "ABC", "AMGN", "ANTM", "BAX", "BDX", "BIO", "BIIB", "BSX", "BMY", "CAH", "CTLT", "CNC", "CERN", "CI", "COO", "CVS", "DHR", "DVA", "XRAY", "DXCM", "EW", "GILD", "HCA", "HSIC", "HOLX", "HUM", "IDXX", "ILMN", "INCY", "ISRG", "IQV", "JNJ", "LH", "LLY", "MCK", "MDT", "MRK", "MTD", "PKI", "PRGO", "PFE", "DGX", "REGN", "RMD", "STE", "SYK", "TFX", "TMO", "UNH", "UHS", "VAR", "VRTX", "VTRS", "WAT", "WST", "ZBH", "ZTS", "MMM", "ALK", "ALLE", "AAL", "AME", "AOS", "BA", "CHRW", "CARR", "CAT", "CTAS", "CPRT", "CSX", "CMI", "DE", "DAL", "DOV", "ETN", "EMR", "EFX", "EXPD", "FAST", "FDX", "FLS", "FTV", "FBHS", "GD", "GE", "GWW", "HON", "HWM", "HII", "IEX", "INFO", "ITW", "IR", "J", "JBHT", "JCI", "KSU", "LHX", "LMT", "MAS", "NLSN", "NSC", "NOC", "ODFL", "OTIS", "PCAR", "PH", "PNR", "PWR", "RTX", "RSG", "RHI", "ROK", "ROL", "ROP", "SNA", "LUV", "SWK", "TDY", "TXT", "TT", "TDG", "UNP", "UAL", "UPS", "URI", "VRSK", "WAB", "WM", "XYL", "ACN", "ADBE", "AMD", "AKAM", "APH", "ADI", "ANSS", "AAPL", "AMAT", "ANET", "ADSK", "ADP", "AVGO", "BR", "CDNS", "CDW", "CSCO", "CTXS", "CTSH", "GLW", "DXC", "FFIV", "FIS", "FISV", "FLT", "FLIR", "FTNT", "IT", "GPN", "HPE", "HPQ", "INTC", "IBM", "INTU", "IPGP", "JKHY", "JNPR", "KEYS", "KLAC", "LRCX", "LDOS", "MA", "MXIM", "MCHP", "MU", "MSFT", "MSI", "NTAP", "NLOK", "NVDA", "ORCL", "PAYX", "PAYC", "PYPL", "QRVO", "QCOM", "CRM", "STX", "NOW", "SWKS", "SNPS", "TEL", "TER", "TXN", "TYL", "VRSN", "V", "VNT", "WDC", "WU", "XRX", "XLNX", "ZBRA", "APD", "ALB", "AMCR", "AVY", "BLL", "CE", "CF", "CTVA", "DOW", "DD", "EMN", "ECL", "FMC", "FCX", "IP", "IFF", "LIN", "LYB", "MLM", "MOS", "NEM", "NUE", "PKG", "PPG", "SEE", "SHW", "VMC", "WRK", "ARE", "AMT", "AVB", "BXP", "CBRE", "CCI", "DLR", "DRE", "EQIX", "EQR", "ESS", "EXR", "FRT", "PEAK", "HST", "IRM", "KIM", "MAA", "PLD", "PSA", "O", "REG", "SBAC", "SPG", "SLG", "UDR", "VTR", "VNO", "WELL", "WY"]

        strategies = [StrategyXII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)


        print("Fundamentals has been queried")


    # Magic Formula only makes sense in Bulk mode
    def test_magic_formula_short(self):
        AlphaAPIDataSource._QA_API_KEY = True
        tickers = ["TSLA", "SNAP"]

        strategies = [StrategyXII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)

    # Magic Formula only makes sense in Bulk mode
    def test_piotroski_score_short(self):
        AlphaAPIDataSource._QA_API_KEY = True
        tickers = ["TSLA", "SNAP"]

        strategies = [StrategyXIII()]

        manager = \
            StrategyManager(
                strategies=strategies,
                tickers=tickers,
                bulk=True
            )

        stocks_per_strategy = manager.stocks_per_strategy
        for stock_per_strategy in stocks_per_strategy:
            for stock in stocks_per_strategy[stock_per_strategy]:
                print(stock.price_info)

if __name__ == '__main__':
    unittest.main()
