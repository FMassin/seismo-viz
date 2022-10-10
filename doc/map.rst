.. ----------------------------------------------------------------------------
.. Title:   Seismological Visualisation 
.. Author:  Fred Massin
.. License: ...
.. ----------------------------------------------------------------------------
.. _chap-map:

Drawing Earthquake Map
======================

...

.. figure:: plots/map.png
   :width: 100%

   Earthquake map
   :label:`figure-earthquake-map` (sources: :source:`apps/plotwms.py`).


Getting the seismological Catalog 
---------------------------------

...

.. code:: python

   >>> import matplotlib.pyplot as plt
   >>> print(plt.rcParams['axes.prop_cycle'].by_key()['color'])
   ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


Drawing the map 
---------------