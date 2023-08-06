===========
rio-ds-mask
===========

A `Rasterio <https://github.com/mapbox/rasterio>`__ plugin for extracting
an image's dataset-level mask.

.. image:: https://travis-ci.org/geowurster/rio-ds-mask.svg?branch=master
    :target: https://travis-ci.org/geowurster/rio-ds-mask

.. image:: https://coveralls.io/repos/github/geowurster/rio-ds-mask/badge.svg?branch=master
    :target: https://coveralls.io/github/geowurster/rio-ds-mask


=====
Usage
=====

.. code-block:: console

    $ rio ds-mask --help
    Usage: rio ds-mask [OPTIONS] INPUT OUTPUT

      Extract an image's dataset-level mask.

      If '--driver' is not given the input driver is used.

    Options:
      -f, --format, --driver TEXT  Output format driver
      --co, --profile NAME=VALUE   Driver specific creation options.See the
                                   documentation for the selected output driver
                                   for more information.
      --help                       Show this message and exit.

This example command creates a singleband ``uint8`` image that is acceptable
to use as a GDAL mask band, meaning that pixels with a value of ``255`` are
transparent and pixels with a vaue of ``0`` are opaque.  The image is
losslessly compressed and internally tiled.

.. code-block:: console

    $ rio ds-mask \
        --driver GTiff \
        tests/data/alpha.tif \
        mask.tif \
        --co COMPRESS=DEFLATE \
        --co TILED=YES


==========
Installing
==========

First `install Rasterio <http://mapbox.github.io/rasterio/installation.html>`__,
then:

.. code-block:: console

    $ pip install rio-ds-mask --user


Developing
==========

.. code-block:: console

    $ git clone https://github.com/geowurster/rio-ds-mask.git
    $ cd rio-ds-mask
    $ pip install -e .\[all\]
    $ pytest --cov rio-ds-mask --cov-report term-missing


License
=======

See `LICENSE.txt <LICENSE.txt>`__


Changelog
=========

See `CHANGES.md <CHANGES.md>`__

