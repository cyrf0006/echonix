![Echonix logo](https://github.com/RobBlackwell/echonix/blob/master/doc/logo.png)

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

Echonix requires a functioning Python 3 distribution and should work
on Windows, Mac OS X or Linux.

The Anaconda Python 3 distribution is recommended and includes
the Spyder integrated development environment which newcomers should
find easy to use and not unlike MATLAB.

Download Echonix and install in a suitable directory on your
system. Ensure that the Echonix top level directory is in your path
(For Spyder, goto Tools -> PYTHONPATH manager).

If you intend working on Echonix and submitting patches then you
probably want to clone the the git repo and install it like this:

```shell
git clone https://github.com/RobBlackwell/echonix.git
cd echonix
pip install -e .
```

## Examples

Look in the examples directory to get started.

## Tools

Some of the Python scripts turn out to be useful command line tools
that can be run from a Unix shell. These are in the tools directory
can can can be symlinked from you bin directory.

## References

398126A_WBAT Reference Manual.pdf,

http://www.simrad.net/ek80_ref_english/default.htm,

https://www.simrad.com/www/01/NOKBG0397.nsf/AllWeb/F2AB311B3F6E6B15C1257106003E0806/$file/164692ad_ek60_reference_manual_english_lores.pdf 

MacLennan, David, and E. John Simmonds. Fisheries acoustics. Vol. 5. Springer Science & Business Media, 2013.
