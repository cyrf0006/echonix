#!/usr/bin/env python3

from echonix import ek60, echogram
from numpy import genfromtxt


# Displays an echogram of an interesting krill swarm at 38kHz

filename = r'../data/tests/stripes.csv'
a = genfromtxt(filename, delimiter=',')

echogram.show(a,
              title='Stripe test',
              cbar_label='Sv (dB)')
