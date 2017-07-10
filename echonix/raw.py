"""Reads and parses Simrad RAW format files and datagrams.

References
----------

The Simrad EK60 Reference Manual,
http://www.simrad.net/ek60_ref_english/default.htm

The Simrad EK80 Reference Manual,
http://www.simrad.net/ek80_ref_english/default.htm

"""

__author__ = 'Rob Blackwell'
__version__ = '0.1'

from collections import namedtuple

import struct
import math
import warnings
import datetime

# Datagrams are defined in the Simrad reference manuals as structures
# of low level C data types. Note that the documentation is, in my
# view, ambiguous about whether integers are signed or unsigned. This
# is my (REB) interpretation as of April 2017:


def read_dword(stream):
    """Reads a DWORD from stream. DWORD is a 32-bit unsigned integer
    (range: 0 through 4294967295 decimal).

    """
    return struct.unpack('I', stream.read(4))[0]


def read_long(stream):
    """Reads a 32-bit signed integer from stream.

    """
    return struct.unpack('i', stream.read(4))[0]


def safe_read_long(stream):
    """Reads a 32-bit signed integer from stream or None if end of file.

    """
    x = stream.read(4)
    if len(x) < 1:
        return None
    else:
        return struct.unpack('i', x)[0]


def write_long(stream, i):
    """Writes a 32-bit signed integer to stream.

    """
    return stream.write(struct.pack('i', i))


def read_short(stream):
    """Reads a 16-bit signed integer from stream.

    """
    return struct.unpack('h', stream.read(2))[0]


def read_float(stream):
    """Reads a 32-bit floating point (IEEE 754) from stream.

    """
    return struct.unpack('f', stream.read(4))[0]


def read_bytes(stream, n):
    """Reads n bytes from stream.

    """
    return stream.read(n)


def write_bytes(stream, bytes):
    """Writes the given bytes to stream.

    """
    return stream.write(bytes)


def read_chars(stream, n):
    """Reads n UTF-8 characters from stream

    """
    # TODO - Should this really be UTF-8 with the possibility of
    # multibyte characters or ASCII?
    return stream.read(n).decode('utf-8')


def read_string(stream, n):
    """Reads a string of n bytes from stream

    """
    return read_chars(stream, n).strip('\0')


def read_floats(stream, n):
    """Reads n floating point numbers from stream.

    """
    return struct.unpack('f'*n, stream.read(4*n))


def read_shorts(stream, n):
    """Reads n shorts from stream.

    """
    return struct.unpack('h'*n, stream.read(2*n))


#
# "The DateTime structure contains a 64-bit integer value stating the
# number of 100 nanosecond intervals since January 1, 1601. This is
# the internal "filetime" used by the Windows NT operating system."
#
# See http://bit.ly/2nYBBL2
#

DateTime = namedtuple('DateTime', ['lowdatetime', 'highdatetime'])


def read_datetime(stream):
    """Reads a Windows NT filetime structure from stream, returning a
DateTime named tuple.

    """
    lowdatetime = read_dword(stream)
    highdatetime = read_dword(stream)
    return DateTime(lowdatetime, highdatetime)


def filetime(d):
    """Returns the filetime being the number of 100 nanosecond intervals
since January 1, 1601 of a given DateTime tuple.

    """
    return d.highdatetime * 4294967296 + d.lowdatetime


def datagram_filetime(datagram):
    """Returns the filetime being the number of 100 nanosecond intervals
since January 1, 1601 for a given datagram.

    """
    d = datagram.dgheader.datetime
    return filetime(d)


def filetime_to_python_datetime(filetime):
    """Converts a filetime to a Python datetime. NB loss of fidelity.

    """
    epoch = datetime.datetime(1601, 1, 1, 0, 0, 0, 0,
                              tzinfo=datetime.timezone.utc)
    m = filetime / 10
    return epoch + datetime.timedelta(microseconds=m)


def python_datetime_to_filetime(d):
    """Converts a Python datetime to filetime being the number of 100
nanosecond intervals since January 1, 1601.

    """
    epoch = datetime.datetime(1601, 1, 1, 0, 0, 0, 0,
                              tzinfo=datetime.timezone.utc)
    d = d - epoch
    filetime = (d.days * 24 * 60 * 60 * 1000000 +
                d.seconds * 1000000 + d.microseconds) * 10
    return filetime


def python_datetime(dt):
    """Returns a Python datetime given a DateTime tuple. NB loss of
fidelity.

    """
    return filetime_to_python_datetime(filetime(dt))


def datagram_python_datetime(datagram):
    """Returns the Python datetime of the given datagram.

    """
    return python_datetime(datagram.dgheader.datetime)


#
# "All datagrams use the same header. The datagram type field
# identifies the type of datagram. ASCII quadruples are used to ease
# human interpretation and long term maintenance; three characters
# identify the datagram type and one character identifies the version
# of the datagram.  The DateTime structure contains a 64-bit integer
# value stating the number of 100 nanosecond intervals since January
# 1, 1601. This is the internal "filetime" used by the Windows NT
# operating system. The data part of the datagram contains any number
# of bytes, and its content is highly datagram dependent."
#


DatagramHeader = namedtuple('DatagramHeader', ['datagramtype', 'datetime'])


def read_datagram_header(stream, length):
    """Reads a datagram of given length from stream, returning just the
header.

    """
    headerlength = 12
    datagramtype = read_chars(stream, 4)
    datetime = read_datetime(stream)

    dgheader = DatagramHeader(datagramtype, datetime)

    n = length - headerlength
    read_bytes(stream, n)
    return dgheader


def read_datagram(stream, length):
    """Reads and parses a datagram of given length from stream.

    """
    headerlength = 12
    datagramtype = read_chars(stream, 4)
    datetime = read_datetime(stream)

    dgheader = DatagramHeader(datagramtype, datetime)

    l = length - headerlength

    if datagramtype == 'XML0':
        datagram = read_xml_datagram(stream, l, dgheader)
    elif datagramtype == 'FIL1':
        datagram = read_binary_datagram(stream, l, dgheader)
    elif datagramtype == 'CON0':
        datagram = read_configuration_datagram(stream, dgheader)
    elif datagramtype == 'NME0':
        datagram = read_text_datagram(stream, l, dgheader)
    elif datagramtype == 'RAW0':
        datagram = read_sample_binary_datagram0(stream, dgheader)
    elif datagramtype == 'RAW3':
        datagram = read_sample_binary_datagram3(stream, dgheader)
    elif datagramtype == 'MRU0':
        datagram = read_mru_binary_datagram(stream, dgheader)
    elif datagramtype == 'TAG0':
        datagram = read_text_datagram(stream, l, dgheader)
    else:
        warnings.warn("No implementation for this datagram")
        datagram = read_binary_datagram(stream, l, dgheader)

    return datagram

# We model datagrams as Python named tuples.

# We define a generic binary datagram consisting of a datagram header
# and a generic array of bytes. This is used as a "catch all" in the
# event that an unknown datagram type is parsed.


BinaryDatagram = namedtuple('BinaryDatagram', ['dgheader', 'bytes'])


def read_binary_datagram(stream, length, dgheader):
    """Creates a generic BinaryDatagram with the given datagram header,
    reading content of length bytes from stream.

    """
    bytes = read_bytes(stream, length)
    return BinaryDatagram(dgheader, bytes)


#
# "XML datagrams are introduced for description of parameters and
# data. They offer more flexibility than binary datagrams with a fixed
# structure, and they are not as compressed as binary datagrams.
#
# XML datagrams are not used for the actual sample data.
#
# The XML datagrams are simply an XML text file following the standard
# XML convention. Tag attributes are used to contain the
# information. The length of the XML file can, as with all types of
# datagrams, be determined from the length of the datagram given in
# the datagram encapsulation.
#
# The name of the first tag defines the contents of the XML datagram
# type.
#
# Currently the following datagram tags are used by the EK80 raw data
# file format.
# Configuration
# The first tag <Configuration> defines the type.
# Environment
# The first tag <Environment> defines the type.
# Parameter
# The first tag <Parameter> defines the type.
#
# Note The Configuration XML datagram replaces the EK60 Configuration
# datagram (Datagram type "CON0").
#
# The Environment XML datagram replaces the environment information
# part of the EK60 Sample datagram (Datagram type "RAW0").
#
# The Parameter XML datagram replaces the parameter information part
# of the EK60 Sample datagram (Datagram type "RAW0")."
#


XMLDatagram = namedtuple('XMLDatagram', ['dgheader', 'xml'])


def read_xml_datagram(stream, length, dgheader):
    """Creates an XMLDatagram with the given datagram header, reading
    content from the given stream.

    """
    xml = read_string(stream, length)
    return XMLDatagram(dgheader, xml)


# "The MRU binary datagram contains motion sensor data at a given
# time.."


MRUDatagram = namedtuple('MRUDatagram', ['dgheader', 'heave', 'roll',
                                         'pitch', 'heading'])


def read_mru_binary_datagram(stream, dgheader):
    """Creates an MRUDatagram with the given datagram header, reading
    content from the given stream.

    """
    heave = read_float(stream)
    roll = read_float(stream)
    pitch = read_float(stream)
    heading = read_float(stream)

    return MRUDatagram(dgheader, heave, roll, pitch, heading)


# The TextDatagram is used for NMEA NME0 and annotation text TAG0
# datagrams.


TextDatagram = namedtuple('TextDatagram', ['dgheader', 'text'])


def read_text_datagram(stream, length, dgheader):
    """Creates a TextDatagram with the given datagram header, reading
    content from the given file.
    """
    text = read_string(stream, length)
    return TextDatagram(dgheader, text)


# EK80 sample binary datagram, RAW3
#
# "The sample datagram contains sample data from each "ping". The
# datagram may have different size and contain different kind of data,
# depending on the DataType parameter."


SampleDatagram3 = namedtuple('SampleDatagram3', ['dgheader', 'channelid',
                                                 'datatype', 'offset',
                                                 'count', 'samples'])


def read_sample_binary_datagram3(stream, dgheader):
    """Creates a SampleDatagram3 (an EK80 RAW3 sample) with the given
    datagram header, reading content from the given stream.

    """
    channelid = read_string(stream, 128)
    datatype = read_short(stream)
    read_chars(stream, 2)  # spare
    offset = read_long(stream)
    count = read_long(stream)

    # The number of values in Samples[] depends on the value of Count
    # and the Datatype.  As an example a DataType decimal value of
    # 1032 means that Samples[] contains ComplexFloat32 samples and
    # that each sample consists of 4 complex numbers (one from each of
    # the 4 transducer quadrants).

    if datatype == 1032:
        samples = read_bytes(stream, 4 * 2 * count * 4)
    else:
        warnings.warn('Datatype {0} not yet implemented'.format(datatype))

    return SampleDatagram3(dgheader, channelid, datatype,
                           offset, count, samples)


# EK60 sample binary datagram, RAW0 The sample datagram contains
# sample data from just one transducer channel. It can contain power
# sample data (Mode = 0), or it can contain both power and angle
# sample data (Mode = 1).

SampleDatagram0 = namedtuple('SampleDatagram0', ['dgheader',
                                                 'channel',
                                                 'mode',
                                                 'transducerdepth',
                                                 'frequency',
                                                 'transmitpower',
                                                 'pulselength',
                                                 'bandwidth',
                                                 'sampleinterval',
                                                 'soundvelocity',
                                                 'absorptioncoefficient',
                                                 'heave', 'txroll',
                                                 'txpitch',
                                                 'temperature',
                                                 'rxroll',
                                                 'rxpitch',
                                                 'offset',
                                                 'count',
                                                 'power',
                                                 'powerdb',
                                                 'angle'])


def read_sample_binary_datagram0(stream, dgheader):
    """Creates a SampleDatagram0 (an EK60 RAW0 sample) with the given
    datagram header, reading content from the given stream.

    """

    # TODO: Find some test data with Mode = 0

    channel = read_short(stream)  # Channel number
    mode = read_short(stream)  # Datatype
    transducerdepth = read_float(stream)  # [m]
    frequency = read_float(stream)  # [Hz]
    transmitpower = read_float(stream)  # [W]
    pulselength = read_float(stream)  # [s]
    bandwidth = read_float(stream)  # [Hz]
    sampleinterval = read_float(stream)  # [s]
    soundvelocity = read_float(stream)  # [m/s]
    absorptioncoefficient = read_float(stream)  # [dB/m]
    heave = read_float(stream)  # [m]
    txroll = read_float(stream)  # [deg]
    txpitch = read_float(stream)  # [deg]
    temperature = read_float(stream)  # [C]
    read_short(stream)  # spare
    read_short(stream)  # spare
    rxroll = read_float(stream)  # [Deg]
    rxpitch = read_float(stream)  # [Deg]
    offset = read_long(stream)  # First sample
    count = read_long(stream)  # Number of samples
    power = read_shorts(stream, count)  # Compressed format - See Remark 1!
    powerdb = [x * (10 * math.log10(2) / 256) for x in power]
    angle = read_shorts(stream, count)  # See Remark 2 below!

    return SampleDatagram0(dgheader, channel, mode, transducerdepth,
                           frequency, transmitpower, pulselength, bandwidth,
                           sampleinterval, soundvelocity,
                           absorptioncoefficient, heave, txroll, txpitch,
                           temperature, rxroll, rxpitch, offset, count,
                           power, powerdb, angle)


# An EK60 configuration datagram consists of a ConfigurationHeader and
# 1 or more ConfigurationTransducer


ConfigurationDatagram = namedtuple('ConfigurationDatagram',
                                   ['dgheader',
                                    'configurationheader',
                                    'configurationtransducer'])


def read_configuration_datagram(stream, dgheader):
    """Creates a ConfigurationDatagram (an EK60 CON0) with the given
    datagram header, reading content from the given stream.

    """
    configurationheader = read_configuration_header(stream)

    n = configurationheader.transducercount
    configurationtransducers = []
    for i in range(0, n):
        configurationtransducer = read_configuration_transducer(stream)
        configurationtransducers.append(configurationtransducer)

    return ConfigurationDatagram(dgheader,
                                 configurationheader,
                                 configurationtransducers)


# A ConfigurationHeader structure is a component of an EK60
# ConfigurationDatagram

ConfigurationHeader = namedtuple('ConfigurationHeader',
                                 ['surveyname',
                                  'transectname',
                                  'soundername',
                                  'version',
                                  'transducercount'])


def read_configuration_header(stream):
    """Reads a ConfigurationHeader structure from the given stream.

    """
    surveyname = read_string(stream, 128)  # "Loch Ness"
    transectname = read_string(stream, 128)
    soundername = read_string(stream, 128)  # "ER60"
    version = read_string(stream, 30)
    read_bytes(stream, 98)  # spare
    transducercount = read_long(stream)  # 1 to 7

    return ConfigurationHeader(surveyname, transectname,
                               soundername, version, transducercount)


# A ConfigurationTransducer structure is a component of an EK60
# ConfigurationDatagram


ConfigurationTransducer = namedtuple('ConfigurationTransducer',
                                     ['channelid',
                                      'beamtype',
                                      'frequency',
                                      'gain',
                                      'equivalentbeamangle',
                                      'beamwidthalongship',
                                      'beamwidthathwartship',
                                      'anglesensitibityalongship',
                                      'anglesensitivityathwartship',
                                      'angleoffsetalongship',
                                      'angleoffsetathwartship',
                                      'posx',
                                      'posy',
                                      'posz',
                                      'dirx',
                                      'diry',
                                      'dirz',
                                      'pulselengthtable',
                                      'gaintable',
                                      'sacorrectiontable',
                                      'gptsoftwareversion'])


def read_configuration_transducer(stream):
    """Reads a ConfigurationTransducer structure from the given stream.

    """
    channelid = read_string(stream, 128)  # Channel identification
    beamtype = read_long(stream)  # 0 = Single, 1 = Split
    frequency = read_float(stream)  # [Hz]
    gain = read_float(stream)  # [dB] - See note below
    equivalentbeamangle = read_float(stream)  # [dB]
    beamwidthalongship = read_float(stream)  # [degree]
    beamwidthathwartship = read_float(stream)  # [degree]
    anglesensitivityalongship = read_float(stream)
    anglesensitivityathwartship = read_float(stream)
    angleoffsetalongship = read_float(stream)  # [degree]
    angleoffsetathwartship = read_float(stream)  # [degree]
    posx = read_float(stream)  # future use
    posy = read_float(stream)  # future use
    posz = read_float(stream)  # future use
    dirx = read_float(stream)  # future use
    diry = read_float(stream)  # future use
    dirz = read_float(stream)  # future use

    # Available pulse lengths for the channel [s]
    pulselengthtable = read_floats(stream, 5)
    read_chars(stream, 8)  # future use
    # Gain for each pulse length in the PulseLengthTable [dB]
    gaintable = read_floats(stream, 5)
    read_chars(stream, 8)  # future use
    # Sa correction for each pulse length in the PulseLengthTable [dB]
    sacorrectiontable = read_floats(stream, 5)
    read_chars(stream, 8)  # spare
    gptsoftwareversion = read_string(stream, 16)
    read_chars(stream, 28)  # spare

    return ConfigurationTransducer(channelid, beamtype, frequency, gain,
                                   equivalentbeamangle, beamwidthalongship,
                                   beamwidthathwartship,
                                   anglesensitivityalongship,
                                   anglesensitivityathwartship,
                                   angleoffsetalongship,
                                   angleoffsetathwartship, posx, posy, posz,
                                   dirx, diry, dirz, pulselengthtable,
                                   gaintable,
                                   sacorrectiontable,
                                   gptsoftwareversion)


def load_raw(filename, datagram_reader=read_datagram):
    """Loads all the datagrams from the file designated by filename.

    A datagram_reader can optionally be specified, being a function
    that takes a stream and a length that must read exactly length
    bytes from said stream. This allows the datagram reading machinery
    to be overriden for example to skip specific datagrams or
    customise parsing.

    """

    # TODO: The spec requires us to check endianness by comparing
    # length fields, but in practice, everyone is using PC/Windows

    datagrams = []

    with open(filename, "rb") as f:
        while True:
            datagram = read_encapsulated_datagram(f, datagram_reader)
            if not datagram:
                break

            datagrams.append(datagram)

    return datagrams


# A standard encapsulation scheme is used for all data files. Each
# datagram is preceded by a 4 byte length tag stating the datagram
# length in bytes. An identical length tag is appended at the end of
# the datagram.

def read_encapsulated_datagram(stream, datagram_reader=read_datagram):
    """Reads an encapsulated datagram from a stream.  Checks the lengths
    and returns a valid datagram tuple.

    """

    length = safe_read_long(stream)
    if length is None:
        return None

    datagram = datagram_reader(stream, length)

    length2 = safe_read_long(stream)
    if length2 is None:
        return None

    if length != length2:
        raise ValueError('Invalid datagram')

    return datagram


def write_datagram(stream, bytes):
    """Writes a datagram consisting of the given bytes to stream in
    encapsulated datagram format, calculating the required length
    header and footer.

    """
    length = len(bytes)

    write_long(stream, length)
    write_bytes(stream, bytes)
    write_long(stream, length)
