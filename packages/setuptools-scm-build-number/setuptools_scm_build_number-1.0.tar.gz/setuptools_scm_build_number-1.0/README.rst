.. image:: https://travis-ci.org/GreatFruitOmsk/setuptools_scm_build_number.svg?branch=master
    :target: https://travis-ci.org/GreatFruitOmsk/setuptools_scm_build_number
    :alt: Travis
.. image:: https://ci.appveyor.com/api/projects/status/abqxn2vbk5k2styb/branch/master?svg=true
    :target: https://ci.appveyor.com/project/GreatFruitOmsk/setuptools_scm_build_number
    :alt: AppVeyor
.. image:: https://codecov.io/gh/GreatFruitOmsk/setuptools_scm_build_number/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/GreatFruitOmsk/setuptools_scm_build_number
    :alt: Coverage
.. image:: https://pyup.io/repos/github/GreatFruitOmsk/setuptools_scm_build_number/shield.svg
    :target: https://pyup.io/repos/github/GreatFruitOmsk/setuptools_scm_build_number/
    :alt: Updates
.. image:: https://img.shields.io/pypi/v/setuptools_scm_build_number.svg
    :target: https://pypi.python.org/pypi/setuptools_scm_build_number
    :alt: PyPI

This is a `setuptools_scm <https://pypi.python.org/pypi/setuptools_scm>`_ plugin
that provides the ``node-date-and-build-number`` local scheme.

Build number is read from the ``BUILD_NUMBER`` environment variable.

Usage
-----

Add ``'setuptools_scm_build_number'`` to the ``setup_requires`` parameter in your
project's ``setup.py`` file:

.. code:: python

    setup(
        ...,
        use_scm_version={
            'local_scheme': 'node-date-and-build-number'
        },
        setup_requires=['setuptools_scm', 'setuptools_scm_build_number'],
        ...,
    )
