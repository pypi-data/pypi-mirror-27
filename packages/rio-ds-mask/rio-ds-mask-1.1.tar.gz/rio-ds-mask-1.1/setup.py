#!/usr/bin/env python


"""Setup script for ``rio-ds-mask``."""


import itertools as it
import os

from setuptools import setup


with open('README.rst') as f:
    readme = f.read().strip()


def parse_dunder_line(string):

    """Take a line like:

        "__version__ = '0.0.8'"

    and turn it into a tuple:

        ('__version__', '0.0.8')

    Not very fault tolerant.
    """

    # Split the line and remove outside quotes
    variable, value = (s.strip() for s in string.split('=')[:2])
    value = value[1:-1].strip()
    return variable, value


with open('rio_ds_mask.py') as f:
    dunders = dict(map(
        parse_dunder_line, filter(lambda l: l.strip().startswith('__'), f)))
    version = dunders['__version__']
    author = dunders['__author__']
    email = dunders['__email__']
    source = dunders['__source__']


extras_require = {
    'test': [
        'pytest>=3',
        'pytest-cov',
        'coveralls',
    ],
}
extras_require['all'] = list(it.chain.from_iterable(extras_require.values()))


setup(
    author=author,
    author_email=email,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: GIS"],
    description="Extract an image's dataset-level mask and write to a new file.",
    entry_points="""    
            [rasterio.rio_plugins]
            ds-mask=rio_ds_mask:rio_ds_mask
    """,
    extras_require=extras_require,
    include_package_data=True,
    install_requires=['click', 'cligj', 'rasterio>=0.36.0'],
    keywords="rasterio plugin dataset mask",
    license="New BSD",
    long_description=readme,
    name="rio-ds-mask",
    py_modules=['rio_ds_mask'],
    url=source,
    version=version,
    zip_safe=True
)
