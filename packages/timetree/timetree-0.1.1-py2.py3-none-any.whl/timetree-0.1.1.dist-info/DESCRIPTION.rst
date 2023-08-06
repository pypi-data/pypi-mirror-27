========
Overview
========



General transformation to make python objects persistent

* Free software: MIT license

Installation
============

::

    pip install timetree

Documentation
=============

https://timetree.readthedocs.io/

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

0.1.0 (2017-10-28)
------------------

* First release on PyPI.


