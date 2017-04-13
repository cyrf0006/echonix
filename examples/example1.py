#!/usr/bin/env python3

from echonix import ek60, echogram

# Displays an echogram of an interesting krill swarm at 38kHz

filename = r'../data/ek60/krill_swarm_20091215/JR230-D20091215-T121917.raw'
frequency = 38000
a, r = ek60.raw_to_sv(filename, frequency)
echogram.show(a, range=r)
