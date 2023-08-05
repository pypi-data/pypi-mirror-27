# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""Convenient module to use main features of silx from the console.

Usage from (I)Python console or notebook:

>>> from silx import sx

With IPython/jupyter, this also runs %pylab.
From the console, it sets-up Qt in order to allow using GUI widgets.
"""

__authors__ = ["T. Vincent"]
__license__ = "MIT"
__date__ = "16/01/2017"


import logging
import sys as _sys


_logger = logging.getLogger(__name__)


# Init logging when used from the console
if hasattr(_sys, 'ps1'):
    logging.basicConfig()

# Probe ipython
try:
    from IPython import get_ipython as _get_ipython
except (NameError, ImportError):
    _get_ipython = None

# Probe ipython/jupyter notebook
if _get_ipython is not None and _get_ipython() is not None:

    # Notebook detection probably fragile
    _IS_NOTEBOOK = ('parent_appname' in _get_ipython().config['IPKernelApp'] or
                    hasattr(_get_ipython(), 'kernel'))
else:
    _IS_NOTEBOOK = False


# Load Qt and widgets only if running from console
if _IS_NOTEBOOK:
    _logger.warning(
        'Not loading silx.gui features: Running from the notebook')

else:
    from silx.gui import qt

    if hasattr(_sys, 'ps1'):  # If from console, make sure QApplication runs
        qapp = qt.QApplication.instance() or qt.QApplication([])

        # Change windows default icon
        from silx.gui import icons as _icons
        qapp.setWindowIcon(_icons.getQIcon('silx'))
        del _icons  # clean-up namespace

    from silx.gui.plot import *  # noqa
    from ._plot import plot, imshow  # noqa


# %pylab
if _get_ipython is not None and _get_ipython() is not None:
    _get_ipython().enable_pylab(gui='inline' if _IS_NOTEBOOK else 'qt')


# Clean-up
del _sys
del _get_ipython
del _IS_NOTEBOOK


# Load some silx stuff in namespace
from silx import *  # noqa
from silx.io import open  # noqa
from silx.io import *  # noqa
from silx.math import Histogramnd, HistogramndLut  # noqa
from silx.math.fit import leastsq  # noqa
