"""Interprets EK60 data from a RAW file.

"""

import math
import numpy as np
from echonix import raw


def raws_to_sv(filenames, frequency):
    """Given a list of filenames designating EK60 RAW files, read those
    RAW files and return a NumPy ndarray of volume backscatter whose
    rows represent pings.  The range in metres is also returned.

    """
    config = None
    pings = []
    r = None
    for filename in filenames:
        with open(filename, "rb") as f:
            while True:
                datagram = raw.read_encapsulated_datagram(f, raw.read_datagram)
                if not datagram:
                    break

                if datagram.dgheader.datagramtype == 'CON0':
                    config = datagram
                elif datagram.dgheader.datagramtype == 'RAW0' \
                        and datagram.frequency == frequency:
                    ping, r = datagram_volume_backscatter(datagram, config)
                    pings.append(ping)
    return np.array(pings), r


def raw_to_sv(filename, frequency):
    """Given a filename designating EK60 RAW files, read the file and
    return a NumPy ndarray of volume backscatter whose rows represent
    pings. The range in metres is also returned.

    """
    return raws_to_sv([filename], frequency)


def mylog10(x):
    """Log10 function which returns -inf for log10(0)

    """
    return math.log10(x) if x != 0 else float("-inf")


def volume_backscatter(pr, f, G, phi, cv, t, alpha, pt,
                       tau, Sac, rangeCorrected):
    """Convert power values to volume backscatter, Sv based on the
    formulae gleaned from the Echoview documentation at
    http://bit.ly/2o1oOrq and old sources of MATLAB EKRaw.

    """

    # TODO: Reconsider the parameter names based on standard acoustics
    # nomenclature described in Simmons and MacLennan.

    tvg = max(0, 20 * mylog10(rangeCorrected))

    l = cv / f  # wavelength

    CSv = 10 * mylog10((pt * (10**(G/10))**2 * l**2 * cv * tau
                        * 10**(phi/10)) / (32 * math.pi**2))

    return pr + tvg + (2 * alpha * rangeCorrected) - CSv - (2*Sac)


def datagram_volume_backscatter(datagram, config):
    """Given a RAW0 datagram and a CON0 datagram as ready by echonix.raw,
    return a NumPy ndarray of volume backscatter Sv.

    """

    # TODO: Clean up

    # TODO: Reconsider variable names based on standard acoustics
    # nomenclature described in Simmons and MacLennan.

    channel = datagram.channel
    f = datagram.frequency

    transducer = config.configurationtransducer[channel-1]

    G = transducer.gain
    phi = transducer.equivalentbeamangle

    cv = datagram.soundvelocity
    t = datagram.sampleinterval
    alpha = datagram.absorptioncoefficient
    pt = datagram.transmitpower
    tau = datagram.pulselength
    dR = cv * t / 2  # calculate sample thickness (in range)

    idx = transducer.pulselengthtable.index(tau)

    Sac = transducer.sacorrectiontable[idx]

    pr = datagram.powerdb

    #rangeCorrected = [(x+1)*dR for x in range(len(pr))]

    # See Echoview documentation http://bit.ly/2pqzS2D for information
    # on range correction

    #tvgCFac = 2

    #rangeCorrected = [max(0, x - tvgCFac * dR) for x in rangeCorrected]

    s = 2 # s is the TvgRangeCorrectionOffset
    rangeCorrected = [max(0, (i + 1) * dR - s * dR) for i in range(len(pr))]

    sv = np.zeros(len(pr))

    for i in range(len(pr)):
        sv[i] = volume_backscatter(pr[i], f, G, phi, cv, t, alpha,
                                   pt, tau, Sac, rangeCorrected[i])

    #total_range = len(pr) * dR
    total_range = rangeCorrected[len(pr)-1]
    return sv, total_range
