Autowire
========

Autowire is light & simple dependency injection library for Python.

You can use dependency injection & resource management without any classes and any magics.

Since python already support nice context manager ([PEP343](https://www.python.org/dev/peps/pep-0343/)),
we don't have to any extra interfaces for setting-up & tearing-down resource.

.. code-block:: python

    from autowire import Resource
    from contextlib import contextmanager

    # Define resources
    db_connection_factory = Resource('db_connection_factory', __name__)
    db_connection = Resource('db_connection', __name__)

    # Implement db_connection resource
    @db_connection.autowire(db_connection_factory)
    @contextmanager
    def with_db_connection(db_connection_factory):
        conn = db_connection_factory()
        try:
            yield conn
        except:
            conn.rollback()
        finally:
            conn.close()


Table of Contents
=================

You can find more guides from following list:

.. toctree::
   :maxdepth: 1

   basics
   use-cases


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
