========
Overview
========



A wrapper around the Text United API written in Python. Each Text United
object is represented by a corresponding Python object. The attributes
of these objects are cached, but the child objects are not.

* Free software: GNU General Public License v3 or later (GPLv3+)

Installation
============

::

    pip install python-textunited

Documentation
=============

https://python-textunited.readthedocs.io/

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

0.1.0 (2017-10-17)
------------------

* First release with the main modules and test working.


