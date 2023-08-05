pytest-env-info
===============

.. image:: https://travis-ci.org/abadger/pytest-env-info.svg?branch=master
    :target: https://travis-ci.org/abadger/pytest-env-info

Push information about the running pytest into the environment


Features
--------

* Injects information about the Python and Pytest versions that are running the unittests into the
  environment.  This can be used for configuring other pytest plugins for the Python version being run
  on.

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


Requirements
------------

* Pytest


Installation
------------

You can install "pytest-env-info" via `pip`_ from `PyPI`_::

    $ pip install pytest-env-info


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-env-info" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/abadger/pytest-env-info/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
