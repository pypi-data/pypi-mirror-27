"""Extract an image's dataset-level mask and write to a new file."""


__version__ = '1.1'
__author__ = 'Kevin Wurster'
__email__ = 'wursterk@gmail.com'
__source__ = 'https://github.com/geowurster/rio-ds-mask'
__license__ = '''
New BSD License

Copyright (c) 2017, Kevin D. Wurster
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* The names of rio-ds-mask or its contributors may not be used to endorse or
  promote products derived from this software without specific prior written
  permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''


import click
import cligj
import rasterio as rio
from rasterio.rio import options


@click.command(name='ds-mask')
@options.file_in_arg
@options.file_out_arg
@cligj.format_opt
@options.creation_options
def rio_ds_mask(input, output, driver, creation_options):

    """Extract an image's dataset-level mask.

    If '--driver' is not given the input driver is used.
    """

    with rio.open(input) as src:

        meta = src.meta.copy()
        meta.update(
            count=1,
            driver=driver or src.driver)

        if creation_options:
            meta.update(**creation_options)

        with rio.open(output, 'w', **meta) as dst:
            for _, window in src.block_windows():
                dst.write(
                    src.dataset_mask(window=window),
                    indexes=1,
                    window=window)
