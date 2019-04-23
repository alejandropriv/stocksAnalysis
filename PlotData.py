import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

class PlotData:


    figure = 1
    plotable_obj = None

    def __init__(self, _plotable_obj):
        PlotData.figure = PlotData.figure + 1
        print("Dataplot {} created".format(self.figure))

        self.plotable_obj = _plotable_obj





    def plot_close(self):
        if self.plotable_obj.data is None:
            print ("Error creating the plot data is null or empty")

        plt.figure(self.figure)
        self.plotable_obj.data['4. close'].plot()
        plt.title('Daily Times Series for the {} stock '.format(self.plotable_obj.symbol))

        plt.show()
        try:
            plt.pause(1)
        except Exception as why:
            print("Error caused by: {}".format(why))


    @staticmethod
    def set_interactive_mode(status):

        if status == True:
            plt.ion()
        else:
            plt.ioff()
