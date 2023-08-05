.. pytest-env-info documentation master file, created by
   sphinx-quickstart on Thu Oct  1 00:43:18 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pytest-env-info's documentation!
===========================================

pytest-env-info provides the Python and Pytest version information in environment variables at
the earliest stage of pytest starting up.  This allows users to configure other plugins using that
information.  This was written specifically to solve the problem of `pytest_cov`_ expanding environment
variables in :file:`.coveragerc` early in pytest startup when the unittests cannot inject these
variables themselves.


Environment Variables
=====================

The following environment variables are set:

.. envvar:: PYTEST_VERSION

    The version of the executing pytest

.. envvar:: PYTEST_PYVER

    The version of the Python interpreter running pytest

.. envvar:: PYTEST_PYMAJVER

    The major version of the Python interpreter.  For instance, "2" on Python-2.7.14 and "3" for
    Python-3.6.1.

.. envvar:: PYTEST_PYMAJMINVER

    The major and minor version of the Python interpreter.  For instance, "2.7" on Python-2.7.14 and
    "3.6" for Python-3.6.1.


Use in configuring coverage
===========================

This plugin was originally written to make configuring `pytest_cov`_'s exclude_lines possible when
run from pytest.  Here's how you can use these values to setup exclusions that vary depending on
whether you run them on Python2 or Python3:

.. code-block:: ini

    # .coveragerc

    [report]
    exclude_lines=
        pragma: no cover
        pragma: (.*, *)?no py(${PYTEST_PYMAJVER}|${PYTEST_PYMAJMINVER}) cover *($|,.*)

The first exclude line is the standard coverage line to exclude a line from coverage reporting.  The
second line is what excludes lines from the coverage report based on whether it is being run on
Python2 or Python3.  The regex in that line says:

* The pattern stars with ``pragma:`` which is just like the standard coverage exclusion.
* Then you can have any combination of comma separated ``no pyMAJ.MINOR cover`` and ``no pyMAJ
  cover`` substrings.  If one of those substrings matches with ``no pyX cover`` or ``no pyX.Y
  cover`` then the line is excluded.

As an example, when run on Python-3.6, the following would all be excluded::

    if six.PY2:  # pragma: no py3 cover
        pass

    if sys.version_info < (3, 5):  # pragma: no py3.5 cover, no py3.6 cover
        pass

The following would not be excluded::

    if six.PY3:  # pragma: no py2 cover
        pass

    if sys.version_info >= (3, 2):  # pragma: no py2 cover,no py3.0 cover, no py3.1 cover
        pass


.. _`pytest_cov`: https://pypi.python.org/pypi/pytest-cov
