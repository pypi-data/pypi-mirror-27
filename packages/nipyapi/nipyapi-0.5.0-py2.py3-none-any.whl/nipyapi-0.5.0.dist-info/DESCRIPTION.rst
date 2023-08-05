=======
NiPyApi
=======

Nifi-Python-Api: A convenient Python wrapper for the Apache NiFi Rest API

.. image:: https://img.shields.io/pypi/v/nipyapi.svg
        :target: https://pypi.python.org/pypi/nipyapi
        :alt: Release Status

.. image:: https://img.shields.io/travis/Chaffelson/nipyapi.svg
        :target: https://travis-ci.org/Chaffelson/nipyapi
        :alt: Build Status

.. image:: https://readthedocs.org/projects/nipyapi/badge/?version=latest
        :target: https://nipyapi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Chaffelson/nipyapi/shield.svg
     :target: https://pyup.io/repos/github/Chaffelson/nipyapi/
     :alt: Python Updates

.. image:: https://coveralls.io/repos/github/Chaffelson/nipyapi/badge.svg?branch=master
    :target: https://coveralls.io/github/Chaffelson/nipyapi?branch=master
    :alt: test coverage

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License


Features
--------

This package provides two main areas of functionality:
    - high-level calls to execute common NiFi tasks:
        - ./nipyapi/canvas.py etc.
    - a full swagger 2.0 compliant NiFi Rest API interface and Datamodels:
        - ./nipyapi/swagger_client/apis/flow_api.py etc.
        - ./nipyapi/swagger_client/models/process_group_entity.py etc.


Background
----------

| For more information on Apache NiFi, please visit `https://nifi.apache.org <https://nifi.apache.org>`_
| For Documentation on this package please visit `https://nipyapi.readthedocs.io. <https://nipyapi.readthedocs.io/en/latest>`_


Version Support
---------------

| Supports NiFi version: 1.2.x
| If you require a different version please raise an `issue <https://github.com/Chaffelson/nipyapi/issues>`_

Requirements
------------

Python 2.7 or 3.6 supported, though other versions may work


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Inspired by the equivalent Java client maintained over at
`hermannpencole/nifi-config <https://github.com/hermannpencole/nifi-config>`_

The swagger 2.0 compliant client auto-generated using the
`Swagger Codegen <https://github.com/swagger-api/swagger-codegen>`_ project,
and then cleaned / bugfixed by the authors.


=======
History
=======

0.4.0 (2017-10-29)
------------------

* Added wrapper functions for many common Template commands (templates.py)
* Added new functions for common Process Groups commands (canvas.py)
* Significant test framework enhancements for wrapper functions
* Many coding style cleanups in preparation for filling out test suite
* Added linting
* Cleaned up docs layout and placement within project
* Integrated with TravisCI
* Dropped Python2.6 testing (wasn't listed as supported anyway)
* Updated examples and Readme to be more informative

0.3.2 (2017-09-04)
------------------

* Fixed bug where tox failing locally due to coveralls expecting travis
* Fixed bug where TravisCI failing due to incorrectly set install requirements
* Fixed bug where swagger_client not importing as expected


0.3.1 (2017-09-04)
------------------

* Fixed imports and requirements for wheel install from PyPi

0.3.0 (2017-09-04)
------------------

* Created basic wrapper structure for future development
* Added simple usage functions to complete todo task
* Added devnotes, updated usage, and various sundry other documentation cleanups
* Split tests into subfolders for better management and clarity
* Added Coveralls and License Badge
* Removed broken venv that ended up in project directory, added similar to ignore file
* Changed default URL in the configuration to default docker url and port on localhost

0.2.1 (2017-08-26)
------------------

* Fixed up removal of leftover swagger client dependencies

0.2.0 (2017-08-25)
------------------

* Merge the nifi swagger client into this repo as a sub package
    * Restructured tests into package subfolders
    * Consolidate package configuration
    * Setup package import structure
    * Updated usage instructions
    * Integrate documentation

0.1.2 (2017-08-24)
------------------

* Created basic integration with nifi-python-swagger-client

0.1.1 (2017-08-24)
------------------

* Cleaned up base project and integrations ready for code migration

0.1.0 (2017-08-24)
------------------

* First release on PyPI.


