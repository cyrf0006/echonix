"""Draws echograms of NumPy ndarrays as used in the echonix library.

"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import numpy.ma as ma
import math

# TODO clean up and refactor show and show_image

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


def show(a, min=None, max=None, range=None, title='Echogram', cbar=True,
         cbar_label=None, xlabel=None,  ylabel=None, show=True):
    """Draws an echogram using the NumPy ndarray a.

    """
    x, y = a.shape
    a = np.transpose(a)

    if min is not None:
        a[a < min] = np.nan

    if max is not None:
        a[a > max] = np.nan

    a = ma.array(a, mask=np.isnan(a))

    colormap = colors.ListedColormap(ek500(), "A")
    plt.pcolormesh(a, cmap=colormap)

    if cbar:
        cbar = plt.colorbar()

        if cbar_label is not None:
            cbar.set_label(cbar_label, rotation=90)

    plt.gca().invert_yaxis()

    if range is None:
        if ylabel is None:
            ylabel = "Bin number"
        #range = y
        top = 0
        bottom = y
    elif isinstance(range, tuple):
        top, bottom = range
    else:
        top = 0
        bottom = range

    if ylabel is None:
        ylabel = "Range / m"

    if xlabel is None:
        xlabel = "Sample"

    stepr = 10**(int(math.log10(bottom-top)))
    stepy = y * stepr / (bottom-top)

    yticks = np.arange(0, y, stepy)
    yticklabels = np.arange(top, bottom, stepr).astype(int)

    if len(yticks) < 3:
        yticks = np.arange(0, y, stepy/5)
        yticklabels = np.arange(top, bottom, stepr/5).astype(int)

    plt.gca().set_yticks(yticks)
    plt.gca().set_yticklabels(yticklabels)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if show:
        plt.show()


def show_image(a, range=None, title='Echogram', xlabel=None, ylabel=None,
               show=True):
    """Draws an echogram like view of the pillow image a. Useful for
displaying composite images.
    """
    x, y = a.size

    if range is None:
        if ylabel is None:
            ylabel = "Bin number"
        #range = y
        top = 0
        bottom = y
    elif isinstance(range, tuple):
        top, bottom = range
    else:
        top = 0
        bottom = range

    stepr = 10**(int(math.log10(bottom-top)))
    stepy = y * stepr / (bottom-top)

    if ylabel is None:
         ylabel = "Range / m"

    if xlabel is None:
        xlabel = "Sample"

    yticks = np.arange(0, y, stepy)
    yticklabels = np.arange(top, bottom, stepr).astype(int)

    if len(yticks) < 3:
        yticks = np.arange(0, y, stepy/5)
        yticklabels = np.arange(top, bottom, stepr/5).astype(int)

    plt.gca().set_yticks(yticks)
    plt.gca().set_yticklabels(yticklabels)

    plt.imshow(a, aspect='auto')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if show:
        plt.show()
