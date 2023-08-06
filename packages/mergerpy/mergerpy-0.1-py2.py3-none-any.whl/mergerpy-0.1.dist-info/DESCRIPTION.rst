MergerPy
========

.. image:: https://codecov.io/gh/abdullahselek/MergerPy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/abdullahselek/MergerPy

.. image:: https://requires.io/github/abdullahselek/MergerPy/requirements.svg?branch=master
    :target: https://requires.io/github/abdullahselek/MergerPy/requirements/?branch=master

+---------------------------------------------------------------------------+------------------------------------------------------------------------------------+
|                                Linux                                      |                                       Windows                                      |
+===========================================================================+====================================================================================+
| .. image:: https://travis-ci.org/abdullahselek/MergerPy.svg?branch=master | .. image:: https://ci.appveyor.com/api/projects/status/5ci6rtapw64u0n1i?svg=true   |
|    :target: https://travis-ci.org/abdullahselek/MergerPy                  |    :target: https://ci.appveyor.com/project/abdullahselek/Mergerpy                 |
+---------------------------------------------------------------------------+------------------------------------------------------------------------------------+

Introduction
============

This library provides a fast text concatenation from files. It works with Python versions from 2.7+ and Python 3.
The main aim to create this library is to create new passwords from given files which contain tokens. Then you can 
use `btcrecover <https://github.com/gurnec/btcrecover>`_ to get your password back.

Sample:

tokens.txt

+------------+
| A 1 e 2 a 3|
+------------+
| B s h i r  | 
+------------+
| E i 34 26 s|
+------------+

New created passwords.txt

+------+
| ABE  |
+------+
| ABi  |
+------+
| AB34 |
+------+
| AB26 |
+------+
| ABs  |
+------+
| ...  |
+------+

Getting the code
================

The code is hosted at https://github.com/abdullahselek/MergerPy

Check out the latest development version anonymously with::

    $ git clone git://github.com/abdullahselek/MergerPy.git
    $ cd MergerPy

To install test dependencies, run::

    $ pip install -Ur requirements.testing.txt

Running Tests
=============

The test suite can be run against a single Python version which requires ``pip install pytest`` and optionally ``pip install pytest-cov`` (these are included if you have installed dependencies from ``requirements.testing.txt``)

To run the unit tests with a single Python version::

    $ py.test -v

to also run code coverage::

    $ py.test --cov=mergerpy

To run the unit tests against a set of Python versions::

    $ tox

Sample Usage
============

With using only one function::

    from mergerpy import merger

    merger.main('tests/resources/sample.txt')

Licence
-------

MergerPy is released under the MIT license. See LICENSE for details.


