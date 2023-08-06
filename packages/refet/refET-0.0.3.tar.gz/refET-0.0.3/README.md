[![Build Status](https://travis-ci.org/cgmorton/RefET.svg?branch=master)](https://travis-ci.org/cgmorton/RefET)
[![coverage](https://codecov.io/gh/cgmorton/RefET/branch/master/graph/badge.svg)](https://codecov.io/gh/cgmorton/RefET)
[![PyPI version](https://badge.fury.io/py/RefET.svg)](https://badge.fury.io/py/RefET)

# ASCE Standardized Reference Evapotranspiration (ET)

NumPy functions for computing daily and hourly reference ET.

## Limitations

The functions have not been tested for multi-dimensional arrays.
Currently the user must handle all of the file I/O and unit conversions.

### Units

The user must convert all input values to the expected units listed below:

type | units
-----|------
temperature (tmin, tmax, tmean) | C
actual vapor pressure (ea) | kPa
solar radiation (rs) | MJ m-2
wind speed (uz) | m s-1
wind speed measurement height (zw) | m
station elevation (elev) | m
latitude (lat) | radians
longitude (lon - hourly only) | radians
time (time - hourly only) | UTC hour at the start of the time period

### Cloudiness Fraction (hourly)

The hourly reference ET calculation is currently performed independently for each time step which causes the cloudiness fraction (fcd) calculation for very low sun angles to be incorrect.

## Installation

To install the RefET python module:
```
pip install refet
```

## Example

To compute a single daily ETr value using weather data for 2015-07-01 from the Fallon, NV AgriMet station.
The necessary unit conversions are shown on the input values.
The raw input data is available [here](https://www.usbr.gov/pn-bin/daily.pl?station=FALN&year=2015&month=7&day=1&year=2015&month=7&day=1&pcode=ETRS&pcode=MN&pcode=MX&pcode=SR&pcode=YM&pcode=UA)

```
import math, refet

# Unit conversions
tmin_c = (66.65 - 32) * (5.0 / 9)
tmax_c = (102.80 - 32) * (5.0 / 9)
tdew_c = (57.26 - 32) * (5.0 / 9)
ea = 0.6108 * math.exp(17.27 * tdew_c / (tdew_c + 237.3))
rs = (674.07 * 0.041868)
uz = 4.80 * 0.44704
lat_radians = (39.4575 * math.pi / 180)

etr = refet.daily(
    tmin=tmin_c, tmax=tmax_c, ea=ea, rs=rs, uz=uz,
    zw=3, elev=1208.5, lat=lat_radians, doy=182, ref_type='etr')

print('ETr: {:.2f} mm'.format(float(etr)))
print('ETr: {:.2f} in'.format(float(etr) / 25.4))
```

## Dependencies

* [numpy](http://www.numpy.org)

Modules needed to run the test suite:
* [pandas](http://pandas.pydata.org)
* [pytest](https://docs.pytest.org/en/latest/)
* [pytz](http://pythonhosted.org/pytz/)

## References

ASCE-EWRI Standardized Reference Evapotranspiration Equation (2005)
* [Report](http://www.kimberly.uidaho.edu/water/asceewri/ascestzdetmain2005.pdf)
* [Appendix](http://www.kimberly.uidaho.edu/water/asceewri/appendix.pdf)
