Autowire
========

.. image:: https://img.shields.io/pypi/v/Autowire.svg
    :alt: PyPI Package Version
    :target: https://pypi.python.org/pypi/Autowire

.. image:: http://readthedocs.org/projects/autowire/badge/?version=latest
    :alt: Documentation Status
    :target: http://autowire.readthedocs.org/en/latest/?badge=latest

.. image:: https://codecov.io/gh/Hardtack/Autowire/branch/develop/graph/badge.svg?token=Xr943HH5xi
    :alt: Codcov Coverage
    :target: https://codecov.io/gh/Hardtack/Autowire

.. image:: https://img.shields.io/github/stars/hardtack/autowire.svg?style=social&label=Star
    :alt: GitHub Stars
    :target: https://github.com/Hardtack/Autowire


Autowire is light & simple dependency injection and resource management library for Python.

You can use dependency injection & resource management without any classes and any magics.

Since python already support nice context manager (`PEP343`_),
we don't have to any extra interfaces for setting-up & tearing-down resource.


.. _PEP343: https://www.python.org/dev/peps/pep-0343/


This is how to define resources in `Autowire`.

.. code-block:: python

    import contextlib
    from autowire import Resource

    # Define resources
    db_connection_factory = Resource("db_connection_factory", __name__)
    db_connection = Resource("db_connection", __name__)

    # Implement db_connection resource
    # db_connection is a resource to be implemented,
    # db_connection_factory is a resource to be injected.
    @db_connection.contextual(db_connection_factory)
    @contextlib.contextmanager
    def with_db_connection(db_connection_factory):
        conn = db_connection_factory()
        try:
            yield conn
        except:
            conn.rollback()
        finally:
            conn.close()


This is how to resolve resource implementations.

.. code-block:: python

    from autowire import Context

    with Context() as context:
        conn = context.resolve(db_connection)
        conn.execute("SELECT * FROM ...")
        ...


Table of Contents
=================

You can find more guides from following list:

.. toctree::
   :maxdepth: 1

   getting-started


API References
==============

.. toctree::
   :maxdepth: 3

   api/modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

External Links
==============

* `GitHub Repository <https://github.com/Hardtack/Autowire>`_

* `PyPI Package <https://pypi.python.org/pypi/Autowire>`_
