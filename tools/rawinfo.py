#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from echonix import raw

# rawinfo.py [FILE]...
# Displays basic metadata about a Simrad RAW file.

def info(filename):

    with open(filename, "rb") as f:
        print("filename: {}".format(filename))

        datagram = raw.read_encapsulated_datagram(f, raw.read_datagram)

        start = raw.filetime(datagram.dgheader.datetime)

        dt = raw.datagram_python_datetime(datagram)
        if datagram.dgheader.datagramtype == 'XML0':
            header = ET.fromstring(datagram.xml).find('Header')
            x = header.attrib['ApplicationName']
            print("type: {}".format(x))
            print('datetime: {}'.format(dt))
        else:
            print("type: {}".format(datagram.configurationheader.soundername))
            print("surveyname: {}".format(
                    datagram.configurationheader.surveyname))
            print('datetime: {}'.format(dt))
            for x in datagram.configurationtransducer:
                print('transducer: {0}'.format(x.channelid))

        n = 1
        while True:

            dgheader = raw.read_encapsulated_datagram(f,
                                                      raw.read_datagram_header)

            if not dgheader:
                break

            n += 1
            end = raw.filetime(dgheader.datetime)

        print("datagrams: {}".format(n))
        print("start: {}".format(start))
        print("end: {}".format(end))


def main():
    for filename in sys.argv[1:]:
        info(filename)


if __name__ == "__main__":
    main()
