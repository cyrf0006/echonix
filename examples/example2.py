#!/usr/bin/env python3

from echonix import raw

# Loads all the datagrams from an EK60 RAW file and displays the
# survey name from the configuration header.

filename = r'../data/ek60/krill_swarm_20091215/JR230-D20091215-T121917.raw'
d = raw.load_raw(filename)
print(d[0].configurationheader.surveyname)
