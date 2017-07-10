#!/usr/bin/env python3

import matplotlib.pyplot as plt
from echonix import ek60, echogram

# Displays an echogram of an interesting krill swarm at 120kHz

filename = r'../data/ek60/krill_swarm_20091215/JR230-D20091215-T121917.raw'
frequency = 120000

Sv, r = ek60.raw_to_sv(filename, frequency)
echogram.egshow(Sv, max = -50, min = -95, range=r)

cbar = plt.colorbar()
cbar.set_label('Sv (dB)', rotation=90)

plt.xlabel('Sample')
plt.ylabel('Range /m')

plt.title('Antarctic krill swarm')

plt.show()
