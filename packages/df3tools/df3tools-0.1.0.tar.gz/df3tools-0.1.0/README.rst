========
df3tools
========

.. image:: https://travis-ci.org/a5kin/df3tools.png?branch=master
    :target: https://travis-ci.org/a5kin/df3tools?branch=master
    :alt: Build Status

.. image:: https://img.shields.io/codeclimate/coverage/github/a5kin/df3tools.svg
    :target: https://codeclimate.com/github/a5kin/df3tools
    :alt: Coverage Status

.. image:: https://img.shields.io/codeclimate/maintainability/a5kin/df3tools.svg
    :target: https://codeclimate.com/github/a5kin/df3tools
    :alt: Maintainability Status

.. image:: https://img.shields.io/scrutinizer/g/a5kin/df3tools.svg
    :target: https://scrutinizer-ci.com/g/a5kin/df3tools/
    :alt: Code Quality

.. image:: https://img.shields.io/pypi/v/df3tools.svg
    :target: https://pypi.org/project/df3tools/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/df3tools.svg
    :target: https://pypi.org/project/df3tools/
    :alt: Supported Python versions

Command-line tools to convert POV-Ray density files (DF3) to a bunch
of images and vice versa.

------------
Installation
------------

The easiest way to install is via standard Python package manager::

    pip install df3tools

Optionally, you may clone package's repository, and run ``setup.py``
script::

    git clone https://github.com/a5kin/df3tools.git
    cd df3tools
    python setup.py install

----------
Quickstart
----------

After successful installation, two tools will be available at
command-line: ``df3split`` and ``df3combine``.

The former, by default, splits density file to a bunch of images and
saves them into ``layerNNN.tga`` files in current directory::

    df3split path-to-original-density-file.df3

The latter, by default, combines all ``layer*`` files in current
directory into a single density file. Image format is auto-detected::

    df3combine path-to-new-density-file.df3

You may also pass an images' prefix like ``-p data/layer``. See the
full list of options below.

--------
df3split
--------

Split POV-Ray ``.df3`` density file to a series of separate images.

Usage
-----
::

    df3split [-h] [-t {tga,png}] [-p PREFIX] [-s] df3file


Positional arguments:
---------------------
::

    df3file    Filename of density file to split.

Optional arguments:
-------------------
::

    -h, --help                        Show help message and exit.
    -t {tga,png}, --format {tga,png}  Output files format.
    -p PREFIX, --prefix PREFIX        Output files prefix.
    -s, --silent                      Suppress output.

----------
df3combine
----------

Combine a series of separate images into POV-Ray ``.df3`` density file.

Usage:
------
::

    df3combine [-h] [-p PREFIX] [-s] df3file

Positional arguments:
---------------------
::

    df3file    Filename of density file to combine images into.

Optional arguments:
-------------------
::

    -h, --help                        Show help message and exit.
    -p PREFIX, --prefix PREFIX        Input files prefix.
    -s, --silent                      Suppress output.

Note, images format is autodetected. You may combine any type of
images, supported by Pillow.

-----
Tests
-----

To run full test suite for all supported Python versions, install
``tox`` package, and run it from project's top directory, containing
``setup.py``::

    pip install tox
    tox

Optionally, you can run tests only for your current Python version by
typing::

    python -m unittest discover -s tests

----------------
Acknowledgements
----------------

Thanks to *Yury Poberezhny* for the idea and motivation to create this
package.
