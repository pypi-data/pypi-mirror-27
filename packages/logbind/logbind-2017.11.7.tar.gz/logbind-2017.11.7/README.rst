.. image:: https://travis-ci.org/cjrh/logbind.svg?branch=master
    :target: https://travis-ci.org/cjrh/logbind

.. image:: https://coveralls.io/repos/github/cjrh/logbind/badge.svg?branch=master
    :target: https://coveralls.io/github/cjrh/logbind?branch=master

.. image:: https://img.shields.io/pypi/pyversions/logbind.svg
    :target: https://pypi.python.org/pypi/logbind

.. image:: https://img.shields.io/github/tag/cjrh/logbind.svg
    :target: https://img.shields.io/github/tag/cjrh/logbind.svg

.. image:: https://img.shields.io/badge/install-pip%20install%20logbind-ff69b4.svg
    :target: https://img.shields.io/badge/install-pip%20install%20logbind-ff69b4.svg

.. image:: https://img.shields.io/pypi/v/logbind.svg
    :target: https://img.shields.io/pypi/v/logbind.svg

.. image:: https://img.shields.io/badge/calver-YYYY.MM.MINOR-22bfda.svg
    :target: http://calver.org/


logbind
======================

Easily bind new fields into your logger instances.

.. code-block:: python

    # Original logger
    logger = logging.getLogger('a')
    logger.info('Hello')

    logger = logbind.bind(logger, id=12345)
    logger.info('Hello')  # <- This logrecord has an extra field "id"

    logger = logbind.bind(logger, abc=67890)
    logger.info('Hello')  # <- logrecord has two extra fields: "id" and "abc"


This feature will be most useful with a structured logging formatter,
such as JSON.  You could try `logjson <https://github.com/cjrh/logjson>`_
for example.
