"""Creates echogram images of NumPy ndarrays as used in the echonix
library.

"""

from PIL import Image
import numpy as np

def threshold(a,  min=None, max=None):

    if min is not None:
        a[a < min] = min

    if max is not None:
        a[a > max] = max

    return a


def composite(r, g, b, min=None, max=None):
    """Returns an RGB composite image given three frequencies, perhaps
Sv38, Sv120 and Sv200

    """

    r = threshold(r, min, max)
    g = threshold(g, min, max)
    b = threshold(b, min, max)

    r = (r - np.nanmin(r)) /(np.nanmax(r) - np.nanmin(r)) * 256
    g = (g - np.nanmin(g)) /(np.nanmax(g) - np.nanmin(g)) * 256
    b = (b - np.nanmin(b)) /(np.nanmax(b) - np.nanmin(b)) * 256

    aa = Image.fromarray(np.uint8(r.transpose()))
    bb = Image.fromarray(np.uint8(g.transpose()))
    cc = Image.fromarray(np.uint8(b.transpose()))

    return Image.merge('RGB', [aa, bb, cc])
