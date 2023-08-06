"""

Description
-----------

 The lagranto package provides classes and function to read, write, plot and
 analyze trajectories (time evolution of air parcels in 3D).


Content
-------

 The following classes are available:

 Tra:           To create a trajectory object
 LagrantoRun:   To calculate trajectories
 CartoFigure:   A class to help plotting trajectories on top of cartopy

 The following function are available:
 plot_trajs:    To plot trajectories on a matplotlib axe
 hhmm2frac:     To convert date in the hhmm format to fraction of hours


Examples
--------

>>> filename = 'lsl_20010313_00.1'
>>> trajs = Tra()
>>> trajs.load_ascii(filename)

>>> filename = 'lsl_20010313_00.4'
>>> trajs = Tra()
>>> trajs.load_netcdf(filename)


"""
from .lagranto import Tra, LagrantoRun
from .formats import hhmm2frac
from .plotting import plot_trajs, CartoFigure
