.. pytest-env-info documentation master file, created by
   sphinx-quickstart on Thu Oct  1 00:43:18 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pytest-env-info's documentation!
===========================================

pytest-env-info provides the Python and Pytest version information in environment variables at
the earliest stage of pytest starting up.  This allows users to configure other plugins using that
information.  This was written specifically to solve the problem of pytest_cov expanding environment
variables in :file:`.coveragerc` early in pytest startup when the unittests cannot inject these
variables themselves.

.. envvar:: PYTEST_VERSION

    The version of the executing pytest

.. envvar:: PYTEST_PYVER

    The version of the Python interpreter running pytest

.. envvar:: PYTEST_PYMAJVER

    The major version of the Python interpreter.  For instance, "2" on Python-2.7.14 and "3" for
    Python-3.6.1.

Contents:

.. toctree::
   :maxdepth: 2




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

