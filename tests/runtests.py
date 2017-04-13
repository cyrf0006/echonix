#!/usr/bin/env python3

# Some simple unit tests for Echonix.py

import math
from echonix import raw
from echonix import ek60
from echonix import echogram


# Test 1 - SONAR equation for EK60

f = 38000.0
G = 25.92
phi = -20.7
cv = 1448.2969
t = 0.000256
alpha = 0.009841439
tau = 0.001024
pt = 1000.0
Sac = -0.49
rangeCorrected = 0
pr = 15.204366577872175

assert math.isclose(ek60.volume_backscatter(pr, f, G, phi, cv, t, alpha, pt,
                                            tau, Sac, rangeCorrected),
                    6.70580814796725)


# Test 2 - Read RAW datagrams

datagrams = raw.load_raw('../data/ek60/jr16003/ek60-sample.raw')

assert datagrams[0].dgheader.datagramtype == "CON0"
assert datagrams[0].configurationheader.surveyname == "JR16003_"
assert len(datagrams[0].configurationtransducer) == 4
assert math.isclose(datagrams[0].configurationtransducer[0].gain,
                    25.92, abs_tol=0.001)
assert len(datagrams) == 4693


# Test 3 - Compute volume backscatter and plot echogram

m, r = ek60.raw_to_sv('../data/ek60/jr16003/ek60-sample.raw', 38000)
echogram.show(m, range=r)

# Test 4 - Load an EK80 file

datagrams = raw.load_raw('../data/ek80/EK80_Example_Data_01/EK80_SimradEcho_WC381_Sequential-D20150513-T090935.raw')
assert len(datagrams) == 461
