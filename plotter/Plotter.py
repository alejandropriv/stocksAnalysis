import abc


class Plotter:

    def __init__():
        pass


    @staticmethod
    def plot_prices_close_adj(prices):
        # Data visualization
        prices.plot()  # Plot of all the stocks superimposed on the same chart


    @staticmethod
    def plot_standard(prices):
        # Standardization
        cp_standardized = \
            (prices - prices.mean()) / prices.std()

        cp_standardized.plot()  # Plot of all the stocks standardized and superimposed on the same chart


    @staticmethod
    def plot_comparative(prices, title, y, x):
        prices.plot(subplots=True, layout=(y, x), title=title,  # TODO: stock.title? stock.meta.title?
                    grid=True)  # Subplots of the stocks
