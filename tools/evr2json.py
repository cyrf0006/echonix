#!/usr/bin/env python3

import sys
import os
from echonix import evr, raw
import datetime
import json

# Takes a list of Echoview region files as arguments, or on stdin,
# parses them and outputs corresponding representations in JSON
# format.

# Start and end are in filetime format (See http://bit.ly/2nYBBL2)

# evr2json *.evr
#
# or
#
# cat *.evr | evr2json.py > regions.json
#
# The latter is convenient for very large batch jobs.


def make_filetime(date, time):
    CCYY = int(date[0:4])
    MM = int(date[4:6])
    DD = int(date[6:8])

    HH = int(time[0:2])
    mm = int(time[2:4])
    SS = int(time[4:6])

    ssss = int(time[6:10])

    d = datetime.datetime(CCYY, MM, DD, HH, mm, SS, 0,
                          tzinfo=datetime.timezone.utc)
    f = raw.python_datetime_to_filetime(d) + (ssss * 1000)
    return(f)


def main():

    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        filenames = sys.stdin

    lst = []
    for filename in filenames:

        filename = filename.rstrip()
        regions = evr.load_evr(filename)

        for region in regions:
            name = region.name
            start = make_filetime(region.bounding_rectangle[0],
                                  region.bounding_rectangle[1])
            top = region.bounding_rectangle[2]
            end = make_filetime(region.bounding_rectangle[3],
                                region.bounding_rectangle[4])
            bottom = region.bounding_rectangle[5]
            points = region.points
            region_type = region.region_type
            classification = region.classification

            lst.append({'filename' : filename,
                        'name' : name,
                        'start' : start,
                        'end' : end,
                        'top' :top,
                        'bottom' : bottom,
                        'points' : points,
                        'region_type' : region_type,
                        'classification' : classification})

        out = os.path.basename(filename) + '.json'
        with open(out, 'w') as f:
            json.dump(lst, f)

if __name__ == "__main__":
    main()
