#!/usr/bin/env python3

from echonix import ek60, echogram
from numpy import genfromtxt

filename = r'../data/tests/stripes.csv'
a = genfromtxt(filename, delimiter=',')

echogram.show(a,
              title='Stripe test',
              cbar_label='Sv (dB)')
