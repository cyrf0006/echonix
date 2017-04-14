#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from echonix import raw

# rawinfo [FILE]
# displays basic metadata about a Simrad RASEW file.

def head(filename):
    with open(filename, "rb") as f:

        datagram = raw.read_encapsulated_datagram(f, raw.read_datagram)

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
            datagram = raw.read_encapsulated_datagram(f, raw.read_datagram)
            if not datagram:
                break
            n += 1

        print("datagrams: {}".format(n))


def main():
    for filename in sys.argv[1:]:
        head(filename)


if __name__ == "__main__":
    main()
