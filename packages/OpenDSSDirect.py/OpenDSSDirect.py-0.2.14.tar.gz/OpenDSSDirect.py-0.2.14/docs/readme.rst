OpenDSSDirect.py
================

|Travis Build Status| |Appveyor Build Status| |codecov| |PyPI|
|Documentation|

OpenDSSDirect.py is a Python package implements a "direct" library
interface to
`OpenDSS <http://smartgrid.epri.com/SimulationTool.aspx>`__. OpenDSS is
an open-source distribution system simulator. See
`OpenDSSDirect.jl <https://github.com/tshort/OpenDSSDirect.jl>`__ for a
similar package in Julia.

**This package is available for Windows, Mac and Linux.**

Documentation
~~~~~~~~~~~~~

The documentation for this package can be found
`here <http://nrel.github.io/OpenDSSDirect.py>`__.

Installation
~~~~~~~~~~~~

**Recommended**: Install Python using Miniconda or Anaconda

Open a command line interface and type the following.

.. code:: bash

    pip install 'OpenDSSDirect.py[extras]'

See
`installation <https://nrel.github.io/OpenDSSDirect.py/notebooks/Installation.html>`__
instructions for more information.

Troubleshooting
~~~~~~~~~~~~~~~

It is recommended to use ``conda`` to install pandas, which is currently
a dependency of this package. This package interfaces with OpenDSS using
the "direct" library interface, so a good understanding of OpenDSS will
help troubleshooting. There are plenty of useful resources located
`here <https://sourceforge.net/p/electricdss/code/HEAD/tree/trunk/Doc/>`__.

If you are having issues using this Python interface, feel free to open
an Issue on GitHub
`here <https://github.com/NREL/OpenDSSDirect.py/issues/new>`__.

Thanks
~~~~~~

Thanks to @tshort, Davis, @temcdrm, @GordStephen and @Muxelmann for
their input and comments.

See @Muxelmann's repo
`here <https://github.com/Muxelmann/OpenDSSDirect.make>`__ on how to
build OpenDSS for Linux.

.. |Travis Build Status| image:: https://travis-ci.org/NREL/OpenDSSDirect.py.svg?branch=master
   :target: https://travis-ci.org/NREL/OpenDSSDirect.py
.. |Appveyor Build Status| image:: https://ci.appveyor.com/api/projects/status/github/NREL/OpenDSSDirect.py?branch=master&svg=true
   :target: https://ci.appveyor.com/project/kdheepak/opendssdirect-py
.. |codecov| image:: https://codecov.io/gh/NREL/OpenDSSDirect.py/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/NREL/OpenDSSDirect.py
.. |PyPI| image:: https://img.shields.io/pypi/v/OpenDSSDirect.py.svg
   :target: https://pypi.python.org/pypi/OpenDSSDirect.py/
.. |Documentation| image:: https://img.shields.io/badge/docs-ready-blue.svg
   :target: http://nrel.github.io/OpenDSSDirect.py
