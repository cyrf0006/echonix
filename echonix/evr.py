"""Reads and parses Echoview 2D Region files.

References
----------

http://support.echoview.com/WebHelp/Reference/File_formats/Export_file_formats/2D_Region_definition_file_format.htm#2D_region_definition_file_format

"""

__author__ = 'Rob Blackwell'
__version__ = '0.1'


from collections import namedtuple


def read_header(f):
    line = f.readline()

    # NB First char is a byte order marker?
    assert(line[1:].startswith('EVRG'))


def read_number_of_regions(f):
    line = f.readline()
    return int(line)


def read_notes(f):
    line = f.readline()
    n = int(line)
    l = []
    for i in range(n):
        l.append(f.readline().strip())
    return l


def read_detection_settings(f):
    line = f.readline()
    n = int(line)
    l = []
    for i in range(n):
        l.append(f.readline().strip())
    return l


def read_region_classification(f):
    line = f.readline().strip()
    return(line)


def read_points(f):
    line = f.readline().strip()
    fields = line.split()
    points = fields[:-1]
    region_type = fields[-1]
    return points, region_type


def read_region_type(f):
    line = f.readline().strip
    return(line)


def read_region_name(f):
    line = f.readline().strip()
    return(line)


def read_blank_line(f):
    line = f.readline().strip()
    assert (line == '')


Region = namedtuple('Region', ['name', 'version', 'classification',
                               'bounding_rectangle',
                               'notes', 'detection_settings', 'points',
                               'region_type'])


def read_region(f):
    read_blank_line(f)

    line = f.readline()
    fields = line.split()
    version = fields[0]
    point_count = fields[1]
    region_id = fields[2]
    region_creation_type = fields[4]
    bounding_rectangle_calculated = fields[6] == '1'
    bounding_rectangle = []
    if bounding_rectangle_calculated:
        # Not enitirely consistent with documentation here?
        date_p1 = fields[7]
        time_p1 = fields[8]
        depth_p1 = fields[9]
        date_p2 = fields[10]
        time_p2 = fields[11]
        depth_p2 = fields[12]
        bounding_rectangle = [date_p1, time_p1, depth_p1,
                              date_p2, time_p2, depth_p2]
    notes = read_notes(f)
    detection_settings = read_detection_settings(f)
    classification = read_region_classification(f)
    points, region_type = read_points(f)
    name = read_region_name(f)

    return Region(name, version, classification, bounding_rectangle,
                  notes, detection_settings, points, region_type)


def load_evr(filename):
    regions = []
    with open(filename) as f:
        read_header(f)
        n = read_number_of_regions(f)
        for i in range(n):
            region = read_region(f)
            regions.append(region)
    return regions
