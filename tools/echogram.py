#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
from echonix import ek60, echogram

# echogram FILE
# Displays a rudimentary echogram of a raw file using matplotlib

# TODO: More command line options, colors, titles etc.


def main():
    filename = sys.argv[1]

    if len(sys.argv) > 2:
        frequency = float(sys.argv[2])
    else:
        frequency = 38000

    a, r = ek60.raw_to_sv(filename, frequency)

    title = "{} kHz echogram".format(frequency / 1000)
    echogram.egshow(a, range=r)

    cbar = plt.colorbar()
    cbar.set_label('Sv (dB)', rotation=90)

    plt.xlabel('Sample')
    plt.ylabel('Range /m')

    plt.title(filename)

    plt.show()



if __name__ == "__main__":
    main()
