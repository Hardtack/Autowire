Use cases
---------

In this page, we will show the common use case of `Autowire`.

For instance, if want to run your application in multiple environment
like development / production, You can change configuration by providing
different values to each contexts.

Suppose that we have resources like that.

.. code-block:: python

    # in resources.py
    from autowire import Resource, impl

    from db_engine import DatabaseEngine

    env = Resource('env', __name__)
    db_config = Resource('db_config', __name__)
    db_connection = Resource('db_connection', __name__)

    @db_config.implement
    @impl.autowired('env', env)
    @impl.plain
    def get_db_config(env):
        path = os.path.join('path/to/config', env, 'db.json')
        with open(path) as f:
            config = json.load(f)
        return config

    @db_connection.implement
    @impl.autowired('db_config', db_config)
    @impl.contextmanager
    def open_db_connection(db_config):
        conn = DatabaseEngine(db_config['HOST'], db_config['PORT'])
        try:
            yield conn
        finally:
            conn.close()


We can change running environment by providing `env` resource

.. code-block:: python

    # app.py
    import os
    from autowire import Context, impl

    from .resources import env, db_connection

    def run(db_connection):
        ...

    app_context = Context()

    app_context.provide(env)
    @impl.plain
    def get_env():
        # Get env from envvar
        return os.environ['APP_ENV']

    # APP_ENV will be injected to env resource.
    with app_context.resolve(db_connection) as conn:
        run(conn)
