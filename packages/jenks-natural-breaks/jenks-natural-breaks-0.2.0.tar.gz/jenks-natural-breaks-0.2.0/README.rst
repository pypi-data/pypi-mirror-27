========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/jenks_natural_breaks/badge/?style=flat
    :target: https://readthedocs.org/projects/jenks_natural_breaks
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/cwalv/jenks_natural_breaks.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/cwalv/jenks_natural_breaks

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/cwalv/jenks_natural_breaks?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/cwalv/jenks_natural_breaks

.. |requires| image:: https://requires.io/github/cwalv/jenks_natural_breaks/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/cwalv/jenks_natural_breaks/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/cwalv/jenks_natural_breaks/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/cwalv/jenks_natural_breaks

.. |version| image:: https://img.shields.io/pypi/v/jenks-natural-breaks.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/jenks-natural-breaks

.. |commits-since| image:: https://img.shields.io/github/commits-since/cwalv/jenks_natural_breaks/v0.2.0.svg
    :alt: Commits since latest release
    :target: https://github.com/cwalv/jenks_natural_breaks/compare/v0.2.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/jenks-natural-breaks.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/jenks-natural-breaks

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/jenks-natural-breaks.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/jenks-natural-breaks

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/jenks-natural-breaks.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/jenks-natural-breaks


.. end-badges

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
