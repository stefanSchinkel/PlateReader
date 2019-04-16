"""DataSet - class to store and plot read data
"""
import random

import numpy as np
import matplotlib.pyplot as plt

CMAPS = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds']

class DataSet(object):
    """Dataset as object"""
    def __init__(self):
        self.row = None
        self.col = None
        self.col_ = None
        self.inner_x = None
        self.inner_y = None
        self.outer_x = None
        self.outer_y = None
        self.labels = []
        self.n_wells = None
        self.data = None

    def __str__(self):
        """Verbose info"""
        return "Dataset with {} wells at {}x{} resolution".format(
                self.n_wells, self.inner_x, self.inner_y)

    def _render(self, title="Result", savename=None, cmap=None):
        """ Render the plot and return to caller

        Args:
            title (str): title of the plot (def: "Result")
            cmap (str): colormap to use (def: random choise)
        """
        # compute some plot parameters
        x_2 = self.inner_x/2
        y_2 = self.inner_y/2
        RADIUS = np.sqrt(x_2**2 + y_2**2)

        ORIGIN = (x_2, y_2)
        LIMITS = [x_2 - RADIUS, y_2 + RADIUS ]
        VMAX = np.amax(self.data)

        fig, axs = plt.subplots(self.outer_x, self.outer_y)
        if not cmap:
            cmap = CMAPS[random.randint(0, len(CMAPS)-1)]

        for row in range(self.outer_x):
            for col in range(self.outer_y):
                idx = row*self.outer_y + col
                ax = axs[row, col]
                c = ax.pcolor(self.data[idx], cmap=cmap, vmin=0, vmax=VMAX)
                circle1 = plt.Circle(ORIGIN, RADIUS, color='k', fill=False)
                ax.add_artist(circle1)
                ax.set_xlim(LIMITS)
                ax.set_ylim(LIMITS)
                ax.axis("off")
                ax.invert_yaxis()
                ax.set_yticklabels([])
                ax.set_xticklabels([])
                ax.set_yticks([])
                ax.set_xticks([])

        fig.suptitle(title)

        return fig

    def show(self, title="Result", cmap=None):
        """ Show the plot
          Args:
            title (str): title of the plot (def: "Result")
            cmap (str): colormap to use (def: random choise)
        """
        fig = self._render(title=title, cmap=cmap)
        plt.show()

    def plot(self, savename, title="Result",  cmap=None):
        """ save the plot
          Args:
            savename (str): path of savefile
            title (str): title of the plot (def: "Result")
            cmap (str): colormap to use (def: random choise)
        """
        fig = self._render(title=title, cmap=cmap)
        plt.savefig(savename)
        plt.close(fig)
        # if not savename:
        #     plt.show()
        # else:
        #     print('saving plot')
        #     FigureCanvas(fig).print_png(savename)
        #     plt.close(fig)
