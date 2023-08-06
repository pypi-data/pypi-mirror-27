=====================================
toll — poor man's integration testing
=====================================

.. image:: https://img.shields.io/pypi/v/toll.svg
        :target: https://pypi.org/project/toll/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/toll.svg
        :target: https://pypi.org/project/toll/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/icemac/toll.svg?branch=master
        :target: https://travis-ci.org/icemac/toll

.. image:: https://readthedocs.org/projects/toll/badge/?version=latest
        :target: https://toll.readthedocs.io/en/latest/
        :alt: Documentation Status

toll = **t**\ est **o**\ ffline **l**\ ocally **l**\ ightweight

Run the tests of multiple configured packages:

* right one package after another

* stopping with the first package which has a failing test

This package is compatible with Python 2.7, 3.4, 3.5, 3.6, PyPy2 and PyPy3.

Documentation see: http://toll.readthedocs.io

This package is licensed under the MIT License, see LICENSE.txt inside the
package.


==========
Change log
==========

4.0 (2017-12-26)
================

- Add an ``ignore-exit-code`` to the configuration of the commands to allow a
  complete run-through of all packages.

- Drop support for Python 3.3.

- Also release as wheel.


3.2 (2017-05-16)
================

- Change license from ZPL to MIT.

- Move canonical repository to https://github.com/icemac/toll.

- Add support for PyPy3.


3.1 (2017-01-07)
================

- Colour the own output of `toll`.

- Add a line above the output for each package.


3.0 (2017-01-06)
================

Backward incompatible changes
-----------------------------

- Add a preconditions to the commands. If the precondition is not met the
  command is not executed. This can be used to prevent running a command in
  a package where it will fail.

  This requires a new config file format. (See documentation.)

Other changes
-------------

- Add support for Python 3.6.


2.1 (2016-12-06)
================

- Add compatibility with `setuptools >= 30.0`.


2.0 (2016-06-17)
================

- Use a default configuration file named ``toll.ini``. This can be overwritten
  using ``-c`` when calling `toll`.

- Allow to specify multiple command which should be called. (See ``--help``.)

- Make package compatible with Python 2.7, 3.3, 3.4 and PyPy.


1.0 (2016-02-26)
================

* Initial release.


