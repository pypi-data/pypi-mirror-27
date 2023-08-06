"""``pytest`` fixtures."""


import os
import shutil

from click.testing import CliRunner
import pytest


@pytest.fixture(scope='function')
def path_alpha_tif(tmpdir):

    """Path to 4 band test file with an alpha band."""

    outfile = str(tmpdir.join('alpha.tif'))
    shutil.copy(os.path.join('tests', 'data', 'alpha.tif'), outfile)
    return outfile


@pytest.fixture(scope='function')
def runner():

    """A standard ``click.testing.CliRunner()``."""

    return CliRunner()
