#!/usr/bin/env python3

import matplotlib.pyplot as plt
from echonix import ek60, echogram
from numpy import genfromtxt

filename = r'../data/tests/stripes.csv'
a = genfromtxt(filename, delimiter=',')

echogram.egshow(a)

cbar = plt.colorbar()
cbar.set_label('Sv (dB)', rotation=90)

plt.xlabel('Sample')
plt.ylabel('Range')

plt.title('Stripe test')

plt.show()
