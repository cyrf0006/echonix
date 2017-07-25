"""Draws echograms of NumPy ndarrays as used in the echonix library.

"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import numpy.ma as ma
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


def egshow(a, min=None, max=None, range=None, cmap=None):
    """Draws an echogram using the NumPy ndarray a.

    """
    x, y = a.shape
    a = np.transpose(a)

    if min is None:
        min = np.nanmin(a)

    if max is None:
        max  = np.nanmax(a)

    if not np.ma.is_masked(a) and np.isnan(a).any():
        a = ma.array(a, mask=np.isnan(a))

    if cmap is None:
        cmap = colors.ListedColormap(ek500(), "A")

    plt.pcolormesh(a, cmap=cmap, vmin = min, vmax = max)

    plt.gca().invert_yaxis()

    if range is None:
        top = 0
        bottom = y
    elif isinstance(range, tuple):
        top, bottom = range
    else:
        top = 0
        bottom = range


    stepr = 10**(int(math.log10(bottom-top)))
    stepy = y * stepr / (bottom-top)

    yticks = np.arange(0, y, stepy)
    yticklabels = np.arange(top, bottom, stepr).astype(int)

    if len(yticks) < 3:
        yticks = np.arange(0, y, stepy/5)
        yticklabels = np.arange(top, bottom, stepr/5).astype(int)

    plt.gca().set_yticks(yticks)
    plt.gca().set_yticklabels(yticklabels)





def imshow(a, range=None, aspect='auto'):
    """Draws an echogram like view of the pillow image a. Useful for
displaying composite images.
    """
    x, y = a.size

    if range is None:
        top = 0
        bottom = y
    elif isinstance(range, tuple):
        top, bottom = range
    else:
        top = 0
        bottom = range

    stepr = 10**(int(math.log10(bottom-top)))
    stepy = y * stepr / (bottom-top)

    yticks = np.arange(0, y, stepy)
    yticklabels = np.arange(top, bottom, stepr).astype(int)

    if len(yticks) < 3:
        yticks = np.arange(0, y, stepy/5)
        yticklabels = np.arange(top, bottom, stepr/5).astype(int)

    plt.gca().set_yticks(yticks)
    plt.gca().set_yticklabels(yticklabels)

    plt.imshow(a, aspect=aspect)

