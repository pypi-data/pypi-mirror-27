python-alkivi-config-manager
============================

|Build Status| |Requirements Status|

Python config-manager used at Alkivi

Package
-------

Example

Write a conf like

.. code:: ini

    [default]
    ; general configuration: default endpoint
    endpoint=dev

    [dev]
    ; configuration specific to 'dev' endpoint
    env=dev

    [prod]
    ; configuration specific to 'prod' endpoint
    env=prod

.. code:: python

    from alkivi.config import ConfigManager
    config = ConfigManager('test')

    # This will look for several files, in order
    # 1. Current working directory: ``./test.conf``
    # 2. Current user's home directory ``~/.test.conf``
    # 3. System wide configuration ``/etc/test.conf``

    # Then find the endpoint
    endpoint = config.get('default', endpoint)

    # Or use a specific one
    endpoint = 'prod'

    # And then
    env = config.get(endpoint, 'env')

Parameters
----------

Tests
-----

Testing is set up using `pytest <http://pytest.org>`__ and coverage is
handled with the pytest-cov plugin.

Run your tests with ``py.test`` in the root directory.

Coverage is ran by default and is set in the ``pytest.ini`` file. To see
an html output of coverage open ``htmlcov/index.html`` after running the
tests.

TODO

Travis CI
---------

There is a ``.travis.yml`` file that is set up to run your tests for
python 2.7 and python 3.2, should you choose to use it.

TODO

.. |Build Status| image:: https://travis-ci.org/alkivi-sas/python-alkivi-config-manager.svg?branch=master
   :target: https://travis-ci.org/alkivi-sas/python-alkivi-config-manager
.. |Requirements Status| image:: https://requires.io/github/alkivi-sas/python-alkivi-config-manager/requirements.svg?branch=master
   :target: https://requires.io/github/alkivi-sas/python-alkivi-config-manager/requirements/?branch=master


