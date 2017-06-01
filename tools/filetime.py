#!/usr/bin/env python3

import sys
import pytz
from echonix import raw
from datetime import datetime

# Convert between filetime and python datetime.
# N.B. filetime is higher resolution than datetime.


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def main():
    arg = sys.argv[1]

    # if it's an integer parse it as a filetime, otherwise
    # assume it's a date string.

    v, b = intTryParse(arg)
    if b:
        print(raw.filetime_to_python_datetime(v))
    else:
        x = datetime.strptime(arg[0:-6], "%Y-%m-%d %H:%M:%S.%f")
        x = x.replace(tzinfo=pytz.UTC)
        x = raw.python_datetime_to_filetime(x)
        print(x)


if __name__ == "__main__":
    main()
