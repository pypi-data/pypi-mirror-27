========
Overview
========



CFFI accelerated Jenks classification

* Free software: MIT license

Installation
============

::

    pip install jenks-natural-breaks

Documentation
=============

https://jenks_natural_breaks.readthedocs.io/

Ported from https://github.com/simple-statistics/simple-statistics

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0 (2017-12-13)
------------------

* First release on PyPI.


