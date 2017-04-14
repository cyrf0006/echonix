#!/usr/bin/env python3

import sys
from echonix import raw

# rawrepair [FILE]
# Attempt to recover datagrams from the start of a corrupted RAW file
# writing good datagrams to a new file repaired.raw

# TODO: Attempt to recover from corrupted packets by searching for
# common datagram headers.

# TODO: BUG don't keet overwriting repaired.raw


def repair(filename):
    with open(filename, "rb") as f:
        with open('repaired.raw', "wb") as w:
            while True:
                print(f.tell())
                datagram = raw.read_encapsulated_datagram(f, raw.read_bytes)
                if not datagram:
                    break
                raw.write_datagram(w, datagram)


def main():
    for filename in sys.argv[1:]:
        repair(filename)


if __name__ == "__main__":
    main()
