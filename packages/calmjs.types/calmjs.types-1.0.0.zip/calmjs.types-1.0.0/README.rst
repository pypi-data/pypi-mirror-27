calmjs.types
============

A collection of types (mostly exception classes) for use with |calmjs|_.

.. image:: https://travis-ci.org/calmjs/calmjs.types.svg?branch=1.0.0
    :target: https://travis-ci.org/calmjs/calmjs.types
.. image:: https://ci.appveyor.com/api/projects/status/iyrgqhraj2qjn1cl/branch/1.0.0?svg=true
    :target: https://ci.appveyor.com/project/metatoaster/calmjs-types/branch/1.0.0
.. image:: https://coveralls.io/repos/github/calmjs/calmjs.types/badge.svg?branch=1.0.0
    :target: https://coveralls.io/github/calmjs/calmjs.types?branch=1.0.0

.. |calmjs| replace:: ``calmjs``
.. |calmjs.types| replace:: ``calmjs.types``
.. _calmjs: https://pypi.python.org/pypi/calmjs


Introduction
------------

Developers of packages and extensions that make use of the Calmjs
toolchain has the option to advise the toolchain with their custom
entry point declarations.  However, to halt the execution they will
need to raise specific exceptions.  This package provides those
exceptions as a separate package, under the MIT Expat license, to avoid
the coupling of the package being developed from the core calmjs
package.


Installation
------------

As this is a developer catered package, the installation should be
optional, and the recommended method is to use the ``install_requires``
or ``setup_requires`` argument for the ``setup`` function call for the
``setup.py`` of the package.

If required, the following command may be executed to source the latest
stable version of |calmjs.types| wheel from PyPI for installation into
the current Python environment.

.. code:: sh

    $ pip install calmjs.parse


Contribute
----------

- Issue Tracker: https://github.com/calmjs/calmjs.types/issues
- Source Code: https://github.com/calmjs/calmjs.types


Legal
-----

The |calmjs.types| package is copyright (c) 2017 Auckland Bioengineering
Institute, University of Auckland.  The |calmjs.types| package is
licensed under the MIT license (specifically, the Expat License).

The Calmjs project is copyright (c) 2017 Auckland Bioengineering
Institute, University of Auckland.
