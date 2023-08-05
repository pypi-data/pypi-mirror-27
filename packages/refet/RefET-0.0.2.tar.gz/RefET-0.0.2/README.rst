.. image:: https://travis-ci.org/cgmorton/RefET.svg?branch=master
  :alt: Travis CI build status
  :target: https://travis-ci.org/cgmorton/RefET
.. image:: https://codecov.io/gh/cgmorton/RefET/branch/master/graph/badge.svg
  :alt: Code Coverage
  :target: https://codecov.io/gh/cgmorton/RefET
.. image:: https://badge.fury.io/py/RefET.svg
  :alt: PyPi Version
  :target: https://badge.fury.io/py/RefET

ASCE Standardized Reference Evapotranspiration (ET) Functions
=============================================================

Generic Python/NumPy functions for computing reference ET for 1d or 2d data.

Limitations
===========
Currently the user must handle all of the file I/O and unit conversions.

The hourly reference ET calculation is currently performed independently for each time step which causes the night time cloudiness fraction (fcd?) calculation to be incorrect.  The impact of this difference is minimal because the reference ET value is so low at night.

Todo
====
The long term goal for this project is to include a "refet" command line utility.

Install
=======
To install the RefET python module:

.. code-block:: python

    pip install refet

Dependencies
============
* `numpy <http://www.numpy.org>`_

Modules needed to run the test suite:

* `pandas <http://pandas.pydata.org>`_
* `pytest <https://docs.pytest.org/en/latest/>`_
* `pytz <http://pythonhosted.org/pytz/>`_

References
==========
ASCE-EWRI Standardized Reference Evapotranspiration Equation

* `Report <http://www.kimberly.uidaho.edu/water/asceewri/ascestzdetmain2005.pdf>`_
* `Appendix <http://www.kimberly.uidaho.edu/water/asceewri/appendix.pdf>`_
