#!/usr/bin/env python3

import matplotlib.pyplot as plt
from echonix import ek60, echogram, imaging

# Displays a composite echogram

filename = r'../data/ek60/krill_swarm_20091215/JR230-D20091215-T121917.raw'

Sv38, r = ek60.raw_to_sv(filename, 38000)
Sv120, r = ek60.raw_to_sv(filename, 120000)
Sv200, r = ek60.raw_to_sv(filename, 200000)

im = imaging.composite(Sv38, Sv120, Sv200, min = -95, max = -50)

echogram.imshow(im, range=r)

plt.xlabel('Sample')
plt.ylabel('Range /m')

plt.title('Antarctic krill swarm')

plt.show()
