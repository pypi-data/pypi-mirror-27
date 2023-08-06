xESMF: Universal Regridder for Geospatial Data
==============================================

|Build Status| |codecov| |docs| |license|

xESMF is a Python package for
`regridding <https://climatedataguide.ucar.edu/climate-data-tools-and-analysis/regridding-overview>`_.
It is

- **Powerful**: It uses ESMF_/ESMPy_ as backend and can regrid between **general curvilinear grids**
  with all `ESMF regridding algorithms <https://www.earthsystemcog.org/projects/esmf/regridding>`_,
  such as **bilinear**, **conservative** and **nearest neighbour**.
- **Easy-to-use**: It abstracts away ESMF's complicated infrastructure
  and provides a simple, high-level API, compatible with xarray_ as well as basic numpy arrays.
- **Fast**: It is faster than ESMPy's original Fortran regridding engine,
  due to the use of the highly-optimized
  `Scipy sparse matrix library <https://docs.scipy.org/doc/scipy/reference/sparse.html>`_.

Please see `online documentation <http://xesmf.readthedocs.io/en/latest/>`_.


.. _ESMF: https://www.earthsystemcog.org/projects/esmf/
.. _ESMPy: https://www.earthsystemcog.org/projects/esmpy/
.. _xarray: http://xarray.pydata.org

.. |Build Status| image:: https://api.travis-ci.org/JiaweiZhuang/xESMF.svg
   :target: https://travis-ci.org/JiaweiZhuang/xESMF
   :alt: travis-ci build status

.. |codecov| image:: https://codecov.io/gh/JiaweiZhuang/xESMF/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/JiaweiZhuang/xESMF
   :alt: code coverage

.. |docs| image:: https://readthedocs.org/projects/xesmf/badge/?version=latest
   :target: http://xesmf.readthedocs.io/en/latest/?badge=latest
   :alt: documentation Status

.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://github.com/JiaweiZhuang/xESMF/blob/master/LICENSE
   :alt: license
