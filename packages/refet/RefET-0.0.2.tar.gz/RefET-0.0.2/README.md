[![Build Status](https://travis-ci.org/cgmorton/RefET.svg?branch=master)](https://travis-ci.org/cgmorton/RefET)
[![codecov](https://codecov.io/gh/cgmorton/RefET/branch/master/graph/badge.svg)](https://codecov.io/gh/cgmorton/RefET)
[![PyPI version](https://badge.fury.io/py/RefET.svg)](https://badge.fury.io/py/RefET)

# ASCE Standardized Reference Evapotranspiration (ET)

Generic Python/NumPy functions for computing reference ET for 1d or 2d data.

## Limitations

Currently the user must handle all of the file I/O and unit conversions.

The hourly reference ET caculation is currently performed independently for each time step which causes the night time cloudiness fraction (fcd?) calculation to be incorrect.  The impact of this difference is minimal because the reference ET value is so low at night.

## Todo

The long term goal for this project is to include a "refet" command line utility and make the module installable using pip (or conda).

## Dependencies

* [numpy](http://www.numpy.org)

Modules needed to run the test suite:
* [pandas](http://pandas.pydata.org)
* [pytest](https://docs.pytest.org/en/latest/)
* [pytz](http://pythonhosted.org/pytz/)

## References

ASCE-EWRI Standardized Reference Evapotranspiration Equation
* [Report](http://www.kimberly.uidaho.edu/water/asceewri/ascestzdetmain2005.pdf)
* [Appendix](http://www.kimberly.uidaho.edu/water/asceewri/appendix.pdf)
