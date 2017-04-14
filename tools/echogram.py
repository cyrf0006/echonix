#!/usr/bin/env python3

import sys
from echonix import ek60
from echonix import echogram

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
    echogram.show(a, range=r, title=title)


if __name__ == "__main__":
    main()
