<div align="center">
  <img src="https://github.com/robblackwell/echonix.py/blob/master/doc/logo.png">
</div>

Hydroacoustic data analysis library for Python with support for EK60
echo sounder data in RAW format.

## Introduction

Acoustic data from scientific echo sounders is typically processed
using proprietary, interactive, graphical software. I wanted tools
that were more suited to automated, unsupervised operation. I also
believe that transparent, repeatable research requires accessible,
open tools.

This library aims to leverage libraries such as NumPy and the wider
Python Scientific computing ecosystem to provide high quality data
analysis tools for hydroacousticians.

__Warning, this software is under active development and should be
considered as alpha quality only. Naming and functionality are still
changing. Accuracy is not guaranteed. Backwards compatibility between
versions is not guaranteed.__

Feedback, comments and pull requests appreciated.


## Quick start

Echonix.py requires a functioning Python 3 distribution and should work
on Windows, Mac OS X or Linux.

The Anaconda Python 3 distribution is recommended and includes
the Spyder integrated development environment which newcomers should
find easy to use and not unlike MATLAB.

Download Echonix.py and install in a suitable directory on your
system. Ensure that the Echonix.py directory is in your path (For
Spyder, goto Tools -> PYTHONPATH manager).

## Simple example

Convert an EK60 raw file to a NumPy array of volume backscatter and
plot an echogram:

```Python
from echonix import ek60, echogram
filename = r'C:\data\yourfile.raw'
frequency = 38000
a, r = ek60.raw_to_sv(filename, frequency)
echogram.show(a, range=r)
```

<img src="https://github.com/robblackwell/echonix.py/blob/master/doc/echogram.png">

## Access to datagrams

The following example loads all tha datagrams from an EK60 RAW file,
creates a list d of datagrams (named tuples) and prints the surveyname
from the configuration header.

```Python
from echonix import raw
filename = r'C:\data\yourfile.raw'
d = raw.load_raw(filename)
print(d[0].configurationheader.surveyname)
```

## References

398126A_WBAT Reference Manual.pdf,

http://www.simrad.net/ek80_ref_english/default.htm,

https://www.simrad.com/www/01/NOKBG0397.nsf/AllWeb/F2AB311B3F6E6B15C1257106003E0806/$file/164692ad_ek60_reference_manual_english_lores.pdf 

MacLennan, David, and E. John Simmonds. Fisheries acoustics. Vol. 5. Springer Science & Business Media, 2013.
