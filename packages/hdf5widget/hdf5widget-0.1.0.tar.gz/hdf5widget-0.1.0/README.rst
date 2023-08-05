HDF5-Widget
===========

|PyPi Version|

This is hdf5widget, a widget for viewing the contents of a
`HDF5 <https://support.hdfgroup.org/HDF5/>`__-file in
`Jupyter <http://jupyter.org/>`__ Notebooks using
`ipywidgets <https://github.com/jupyter-widgets/ipywidgets>`__.

Install
-------

Installing with pip
~~~~~~~~~~~~~~~~~~~

::

    pip install hdf5widget

Installing with conda
~~~~~~~~~~~~~~~~~~~~~

::

    conda install -c mrossi hdf5widget

Usage
-----

Assume you have a HDF-file ``file.hdf5``.

.. code:: python

    from hdf5widget import HDF5Widget

    HDF5Widget('file.hdf5').widget

.. |PyPi Version| image:: https://img.shields.io/pypi/v/hdf5widget.svg
   :target: https://pypi.python.org/pypi/hdf5widget
