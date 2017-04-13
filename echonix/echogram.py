"""Draws echograms of NumPy ndarrays as used in the echonix library.

"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import math


def ek500():
    """ek500 - return a 13x3 array of RGB values representing the Simrad
EK500 color table

    """

    rgb = [(1, 1, 1),
           (159/255, 159/255, 159/255),
           (95/255, 95/255, 95/255),
           (0, 0, 1),
           (0, 0, 127/255),
           (0, 191/255, 0),
           (0, 127/255, 0),
           (1, 1, 0),
           (1, 127/255, 0),
           (1, 0, 191/255),
           (1, 0, 0),
           (166/255, 83/255, 60/255),
           (120/255, 60/255, 40/255)]
    return rgb


def show(a, min=-90, max=-30, range=None, title='Echogram'):
    """Draws an echogram using the NumPy ndarray a.

    """
    x, y = a.shape
    a = np.transpose(a)
    a[a < min] = min
    a[a > max] = max
    colormap = colors.ListedColormap(ek500(), "A")
    plt.pcolormesh(a, cmap=colormap)
    plt.colorbar()
    plt.gca().invert_yaxis()

    if range is None:
        range = y

    stepr = 10**(int(math.log10(range)))
    stepy = y * stepr / range

    yticks = np.arange(0, y, stepy)
    yticklabels = np.arange(0, range, stepr)

    if len(yticks) < 3:
        yticks = np.arange(0, y, stepy/5)
        yticklabels = np.arange(0, range, stepr/5)

    plt.gca().set_yticks(yticks)
    plt.gca().set_yticklabels(yticklabels)

    plt.title(title)
    plt.xlabel("Sample")
    plt.ylabel("Range / m")
    plt.show()
