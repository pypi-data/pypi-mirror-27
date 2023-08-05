========
Overview
========



This is the home of the documentation for pyDiffMap, an open-source project to develop a robust and accessible diffusion map code for public use. Our documentation is currently under construction, please bear with us.

* Free software: GPL

Installation
============

Pydiffmap is installable using pip.  You can install it using the command

::

    pip install pyDiffMap

In the meantime, you can install the package directly from the source directly by downloading the package from github and running the command below, optionally with the "-e" flag for an editable install.

::

    pip install [source_directory]

Documentation
=============

https://pyDiffMap.readthedocs.io/

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

If you don't have tox installed, you can also run the python tests directly with 

::

    pytest



Changelog
=========

0.1.0 (2017-12-06)
------------------

* Added base functionality to the code.


