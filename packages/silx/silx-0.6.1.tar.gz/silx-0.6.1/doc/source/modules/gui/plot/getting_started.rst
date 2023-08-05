.. currentmodule:: silx.gui

Getting started with plot widgets
=================================

This introduction to :mod:`silx.gui.plot` covers the following topics:

- `Use silx.gui.plot from the console`_
- `Use silx.gui.plot from a script`_
- `Plot curves in a widget`_
- `Plot images in a widget`_
- `Control plot axes`_

For a complete description of the API, see :mod:`silx.gui.plot`.

Use :mod:`silx.gui.plot` from the console
-----------------------------------------

From IPython
++++++++++++

To run :mod:`silx.gui.plot` widgets from `IPython <http://ipython.org/>`_, IPython must be set to use Qt (and in case of using PyQt4 and Python 2.7, PyQt must be set ti use API version 2, see Explanation_ below).

As *silx* is performing some configuration of the Qt binding and `matplotlib <http://matplotlib.org/>`_, the safest way to use *silx* from IPython is to import :mod:`silx.gui.plot` first and then run either `%gui <http://ipython.org/ipython-doc/stable/interactive/magics.html#magic-gui>`_ qt  or `%pylab <http://ipython.org/ipython-doc/stable/interactive/magics.html#magic-pylab>`_ qt::

  In [1]: from silx.gui.plot import *
  In [2]: %pylab qt

Alternatively, when using Python 2.7 and PyQt4, you can start IPython with the ``QT_API`` environment variable set to ``pyqt``.

On Linux and MacOS X, run::

  QT_API=pyqt ipython

On Windows, run from the command line::

  set QT_API=pyqt&&ipython


Explanation
...........

PyQt4 used from Python 2.x provides 2 incompatible versions of QString and QVariant:

- version 1, the legacy which is the default, and
- version 2, a more pythonic one, which is the only one supported by *silx*.

All other configurations (i.e., PyQt4 on Python 3.x, PySide, PyQt5, IPython QtConsole widget) uses version 2 only or as the default.

For more information, see `IPython, PyQt and PySide <http://ipython.org/ipython-doc/stable/interactive/reference.html#pyqt-and-pyside>`_.


From Python
+++++++++++

The :mod:`silx.sx` package is a convenient module to use silx from the console.
It sets-up Qt and provides functions for the main features of silx.

>>> from silx import sx

Alternatively, you can create a QApplication before using silx widgets:

>>> from silx.gui import qt  # Import Qt binding and do some set-up
>>> qapp = qt.QApplication([])

>>> from silx.gui.plot import *  # Import plot widgets and set-up matplotlib

.. currentmodule:: silx.sx

Plot functions
++++++++++++++

The :mod:`silx.sx` package provides 2 functions to plot curves and images from the (I)Python console in a widget with a set of tools:

- :func:`plot`, and
- :func:`imshow`.

For more features, use widgets directly (see `Plot curves in a widget`_ and `Plot images in a widget`_).


Curve: :func:`plot`
...................

The following examples must run with a Qt QApplication initialized (see `Use silx.gui.plot from the console`_).

First import :mod:`sx` function:

>>> from silx import sx
>>> import numpy

Plot a single curve given some values:

>>> values = numpy.random.random(100)
>>> plot_1curve = sx.plot(values, title='Random data')

Plot a single curve given the x and y values:

>>> angles = numpy.linspace(0, numpy.pi, 100)
>>> sin_a = numpy.sin(angles)
>>> plot_sinus = sx.plot(angles, sin_a,
...                      xlabel='angle (radian)', ylabel='sin(a)')

Plot many curves by giving a 2D array, provided xn, yn arrays:

>>> plot_curves = sx.plot(x0, y0, x1, y1, x2, y2, ...)

Plot curve with style giving a style string:

>>> plot_styled = sx.plot(x0, y0, 'ro-', x1, y1, 'b.')

See :func:`plot` for details.


Image: :func:`imshow`
.....................

This example plot a single image.

First, import :mod:`silx.sx`:

>>> from silx import sx
>>> import numpy

>>> data = numpy.random.random(1024 * 1024).reshape(1024, 1024)
>>> plt = sx.imshow(data, title='Random data')

See :func:`imshow` for more details.


Use :mod:`silx.gui.plot` from a script
--------------------------------------

A Qt GUI script must have a QApplication initialized before creating widgets:

.. code-block:: python

   from silx.gui import qt

   [...]

   qapp = qt.QApplication([])

   [...] # Widgets initialisation

   if __name__ == '__main__':
       [...]
       qapp.exec_()

Unless a Qt binding has already been loaded, :mod:`silx.gui.qt` uses the first Qt binding it founds by probing in the following order: PyQt5, PyQt4 and finally PySide.
If you prefer to choose the Qt binding yourself, import it before importing
a module from :mod:`silx.gui`:

.. code-block:: python

   import PySide  # Importing PySide will force silx to use it
   from silx.gui import qt


.. warning::

   :mod:`silx.gui.plot` widgets are not thread-safe.
   All calls to :mod:`silx.gui.plot` widgets must be made from the main thread.

Plot curves in a widget
-----------------------

The :class:`Plot1D` widget provides a plotting area and a toolbar with tools useful for curves such as setting logarithmic scale or defining region of interest.

First, create a :class:`Plot1D` widget:

.. code-block:: python

   from silx.gui.plot import Plot1D

   plot = Plot1D()  # Create the plot widget
   plot.show()  # Make the plot widget visible


One curve
+++++++++

To display a single curve, use the :meth:`.PlotWidget.addCurve` method:

.. code-block:: python

   plot.addCurve(x=(1, 2, 3), y=(3, 2, 1))  # Add a curve with default style

When you need to update this curve, call :meth:`.PlotWidget.addCurve` again with the new values to display:

.. code-block:: python

   plot.addCurve(x=(1, 2, 3), y=(1, 2, 3))  # Replace the existing curve

To clear the plotting area, call :meth:`.PlotWidget.clear`:

.. code-block:: python

   plot.clear()


Multiple curves
+++++++++++++++

In order to display multiple curves at the same time, you need to provide a different ``legend`` string for each of them:

.. code-block:: python

   import numpy

   x = numpy.linspace(-numpy.pi, numpy.pi, 1000)
   plot.addCurve(x, numpy.sin(x), legend='sinus')
   plot.addCurve(x, numpy.cos(x), legend='cosinus')
   plot.addCurve(x, numpy.random.random(len(x)), legend='random')


To update a curve, call :meth:`.PlotWidget.addCurve` with the ``legend`` of the curve you want to udpdate.
By default, the new curve will keep the same color (and style) as the curve it is updating:

.. code-block:: python

   plot.addCurve(x, numpy.random.random(len(x)) - 1., legend='random')

To remove a curve from the plot, call :meth:`.PlotWidget.remove` with the ``legend`` of the curve you want to remove from the plot:

.. code-block:: python

   plot.remove('random')

To clear the plotting area, call :meth:`.PlotWidget.clear`:

.. code-block:: python

   plot.clear()

Curve style
+++++++++++

By default, different curves will automatically use different styles to render, and keep the same style when updated.

It is possible to specify the ``color`` of the curve, its ``linewidth`` and ``linestyle`` as well as the ``symbol`` to use as markers for data points (See :meth:`.PlotWidget.addCurve` for more details):

.. code-block:: python

   import numpy

   x = numpy.linspace(-numpy.pi, numpy.pi, 100)

   # Curve with a thick dashed line
   plot.addCurve(x, numpy.sin(x), legend='sinus',
                 linewidth=3, linestyle='--')

   # Curve with pink markers only
   plot.addCurve(x, numpy.cos(x), legend='cosinus',
                 color='pink', linestyle=' ', symbol='o')

   # Curve with green line with square markers
   plot.addCurve(x, numpy.random.random(len(x)), legend='random',
                 color='green', linestyle='-', symbol='s')



Histogram
+++++++++

Data can be displayed as an histogram. This must be specified when calling the the addCurve function. (using ``histogram``, See :meth:`.PlotWidget.addCurve` for more details ).

Histogram steps can be centered on x values or set at the left or the right of the given x values.

.. code-block:: python
  
    import numpy
    x = numpy.arange(0, 20, 1)
    plot.addCurve(x, x+1, histogram='center', fill=True, color='green')

.. note:: You can also give x as edges. For this you must have len(x) = len(y) + 1

Plot images in a widget
-----------------------

The :class:`Plot2D` widget provides a plotting area and a toolbar with tools useful for images, such as keeping aspect ratio, changing the colormap or defining a mask.

First, create a :class:`Plot2D` widget:

.. code-block:: python

   from silx.gui.plot import Plot2D

   plot = Plot2D()  # Create the plot widget
   plot.show()  # Make the plot widget visible


One image
+++++++++

To display a single image, use the :meth:`.PlotWidget.addImage` method:

.. code-block:: python

   import numpy

   data = numpy.random.random(512 * 512).reshape(512, -1)  # Create 2D image
   plot.addImage(data)  # Plot the 2D data set with default colormap


To update this image, call :meth:`.PlotWidget.addImage` again with the new image to display:

.. code-block:: python

   # Create a RGB image
   rgb_image = (numpy.random.random(512*512*3) * 255).astype(numpy.uint8)
   rgb_image.shape = 512, 512, 3

   plot.addImage(rgb_image)  # Plot the RGB image instead of the previous data


To clear the plotting area, call :meth:`.PlotWidget.clear`:

.. code-block:: python

   plot.clear()


Origin and scale
++++++++++++++++

:meth:`.PlotWidget.addImage` supports both 2D arrays of data displayed with a colormap and RGB(A) images as 3D arrays of shape (height, width, color channels).

When displaying an image, it is possible to specify the ``origin`` and the ``scale`` of the image array in the plot area coordinates:

.. code-block:: python

   data = numpy.random.random(512 * 512).reshape(512, -1)
   plot.addImage(data, origin=(100, 100), scale=(0.1, 0.1))

When updating an image, if ``origin`` and ``scale`` are not provided, the previous values will be used:

.. code-block:: python

   data = numpy.random.random(512 * 512).reshape(512, -1)
   plot.addImage(data)  # Keep previous origin and scale


Colormap
++++++++

A ``colormap`` is described with a :class:`.Colormap` class as follows:

.. code-block:: python

   colormap = Colormap(name='gray',             # Name of the colormap
                       normalization='linear',  # Either 'linear' or 'log'
                       vmin=0.0,                # If not autoscale, data value to bind to min of colormap
                       vmax=1.0                 # If not autoscale, data value to bind to max of colormap
               )


At least the following colormap names are guaranteed to be available, but any colormap name from `matplotlib <http://matplotlib.org/>`_ (see `Choosing Colormaps <http://matplotlib.org/users/colormaps.html>`_) should work:

- gray
- reversed gray
- temperature
- red
- green
- blue
- viridis
- magma
- inferno
- plasma

It is possible to change the default colormap of :meth:`.PlotWidget.addImage` for the plot widget with :meth:`.PlotWidget.setDefaultColormap` (and to get it with :meth:`.PlotWidget.getDefaultColormap`):

.. code-block:: python

   colormap = Colormap(name='viridis',
                       normalization='linear',
                       vmin=0.0,
                       vmax=1.0)
   plot.setDefaultColormap(colormap)

   data = numpy.arange(512 * 512.).reshape(512, -1)
   plot.addImage(data)  # Rendered with the default colormap set before

It is also possible to provide a :class:`.Colormap` to :meth:`.PlotWidget.addImage` to override this default for an image:

.. code-block:: python

   colormap = Colormap(name='magma',
                       normalization='log',
                       vmin=1.2,
                       vmax=1.8)
   data = numpy.random.random(512 * 512).reshape(512, -1) + 1.
   plot.addImage(data, colormap=colormap)

As for `Origin and scale`_, when updating an image, if ``colormap`` is not provided, the previous colormap will be used:

.. code-block:: python

   data = numpy.random.random(512 * 512).reshape(512, -1) + 1.
   plot.addImage(data)  # Keep previous colormap

The colormap can be changed by the user from the widget's toolbar.


Multiple images
+++++++++++++++

In order to display multiple images at the same time, you need to provide a different ``legend`` string for each of them and to set the ``replace`` argument to ``False``:

.. code-block:: python

   data = numpy.random.random(512 * 512).reshape(512, -1)
   plot.addImage(data, legend='random', replace=False)

   data = numpy.arange(512 * 512.).reshape(512, -1)
   plot.addImage(data, legend='arange', replace=False, origin=(512, 512))


To update an image, call :meth:`.PlotWidget.addImage` with the ``legend`` of the curve you want to udpdate.
By default, the new image will keep the same colormap, origin and scale as the image it is updating:

.. code-block:: python

   data = (512 * 512. - numpy.arange(512 * 512.)).reshape(512, -1)
   plot.addImage(data, legend='arange', replace=False)  # Beware of replace=False


To remove an image from the plot, call :meth:`.PlotWidget.remove` with the ``legend`` of the image you want to remove:

.. code-block:: python

   plot.remove('random')


Control plot axes
-----------------

The following examples illustrate the API to control the plot axes.
:meth:`.PlotWidget.getXAxis` and :meth:`.PlotWidget.getYAxis` give access to each plot axis (:class:`.items.Axis`) in order to control them.

Labels and title
++++++++++++++++

Use :meth:`.PlotWidget.setGraphTitle` to set the plot main title.
Use :meth:`.PlotWidget.getXAxis` and :meth:`.PlotWidget.getYAxis` to get the axes and set their text label with :meth:`.items.Axis.setLabel`:

.. code-block:: python

   plot.setGraphTitle('My plot')
   plot.getXAxis().setLabel('X')
   plot.getYAxis().setLabel('Y')


Axes limits
+++++++++++

Different methods allows to get and set the data limits displayed on each axis.

The following code moves the visible plot area to the right:

.. code-block:: python

    xmin, xmax = plot.getXAxis().getLimits()
    offset = 0.1 * (xmax - xmin)
    plot.getXAxis().setLimits(xmin + offset, xmax + offset)

:meth:`.PlotWidget.resetZoom` set the plot limits to the bounds of the data:

.. code-block:: python

   plot.resetZoom()

See :meth:`.PlotWidget.resetZoom`, :meth:`.PlotWidget.setLimits`, :meth:`.PlotWidget.getXAxis`, :meth:`.PlotWidget.getYAxis` and :class:`.items.Axis` for details.


Axes
++++

Different methods allow plot axes modifications:

.. code-block:: python

   plot.getYAxis().setInverted(True)  # Makes the Y axis pointing downward
   plot.setKeepDataAspectRatio(True)  # To keep aspect ratio between X and Y axes

See :meth:`.PlotWidget.getYAxis`, :meth:`.PlotWidget.setKeepDataAspectRatio` for details.

.. code-block:: python

   plot.setGraphGrid(which='both')  # To show a grid for both minor and major axes ticks

   # Use logarithmic axes
   plot.getXAxis().setScale("log")
   plot.getYAxis().setScale("log")

See :meth:`.PlotWidget.setGraphGrid`, :meth:`.PlotWidget.getXAxis`, :meth:`.PlotWidget.getXAxis` and :class:`.items.Axis` for details.
