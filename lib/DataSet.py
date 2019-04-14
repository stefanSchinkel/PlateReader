"""DataSet - class to store and plot read data
"""
import random

import numpy as np
import matplotlib.pyplot as plt

CMAPS = [
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'
    ]

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

    def plot(self, plot_name="result", savename=None):
        """ Plot the data
        """
        # compute some plot parameters
        x_2 = self.inner_x/2
        y_2 = self.inner_y/2
        RADIUS = np.sqrt(x_2**2 + y_2**2)

        ORIGIN = (x_2, y_2)
        LIMITS = [x_2 - RADIUS, y_2 + RADIUS ]
        VMAX = np.amax(self.data)

        fig, axs = plt.subplots(self.outer_x, self.outer_y)

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

        fig.suptitle(plot_name)

        if not savename:
            plt.show()
        else:
            plt.savefig(savename)
            plt.close(fig)
