#!/usr/bin/env python3

import sys
from echonix import raw

# rawnmea [FILE]
# Extracts NMEA strings from RAW files.

def nmea_sentences(filename):
    with open(filename, "rb") as f:
        while True:
            datagram = raw.read_encapsulated_datagram(f, raw.read_datagram)
            if not datagram:
                break
            if datagram.dgheader.datagramtype == 'NME0':
                print(datagram.text)


def main():
    for filename in sys.argv[1:]:
        nmea_sentences(filename)


if __name__ == "__main__":
    main()
