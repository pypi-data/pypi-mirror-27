.. _lagranto-package:

Basic examples
--------------

In a first step, let's simply read the trajectories::

    >>> from lagranto import Tra
    >>> filename = 'lsl_20110123_10'
    >>> trajs = Tra()
    >>> trajs.load_ascii(filename)

or to read a netcdf file::

    >>> filename = 'lsl_20110123_10.4'
    >>> trajs.load_netcdf(filename)

The proprieties of the trajectories can be shown as follow::
    >>> print(trajs)
    24 trajectories with 41 time steps.
    Available fields: time/lon/lat/p/Q/RH/TH/BLH
    total duration: -14400.0 minutes
    >>> print(trajs.variables())
    ['time', 'lon', 'lat', 'p', 'Q', 'RH', 'TH', 'BLH']
    >>> print(trajs['Q'].shape)
    (24, 41)

   
DocStrings
----------

Tra
~~~

.. autoclass:: lagranto.Tra
  :members:


LagrantoRun
~~~~~~~~~~~

.. autoclass:: lagranto.LagrantoRun
  :members:
