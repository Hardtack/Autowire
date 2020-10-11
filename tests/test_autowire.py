import os

from autowire import Context, Resource, impl, resource


def test_autowire():
    config_dir = Resource("config_dir", __name__)
    db_config = Resource("db_config", __name__)

    @db_config.implement
    @impl.autowired("config_dir", config_dir)
    @impl.contextmanager
    def db_config_path(config_dir):
        yield os.path.join(config_dir, "database.yml")

    dev_context = Context()
    prod_context = Context()

    @dev_context.provide(config_dir)
    @impl.plain
    def get_dev_config_dir():
        return "./config/"

    @prod_context.provide(config_dir)
    @impl.plain
    def get_prod_config_dir():
        return "/etc/autowire/"

    with dev_context.resolve(db_config) as dev_db_config:
        assert (
            os.path.join(get_dev_config_dir(), "database.yml") == dev_db_config
        )

    with prod_context.resolve(db_config) as prod_db_config:
        assert (
            os.path.join(get_prod_config_dir(), "database.yml")
            == prod_db_config
        )


def test_autowire_plain():
    config_dir = Resource("config_dir", __name__)
    db_config = Resource("db_config", __name__)

    @db_config.implement
    @impl.autowired("config_dir", config_dir)
    @impl.plain
    def db_config_path(config_dir):
        return os.path.join(config_dir, "database.yml")

    dev_context = Context()
    prod_context = Context()

    @dev_context.provide(config_dir)
    @impl.plain
    def get_dev_config_dir():
        return "./config/"

    @prod_context.provide(config_dir)
    @impl.plain
    def get_prod_config_dir():
        return "/etc/autowire/"

    with dev_context.resolve(db_config) as dev_db_config:
        assert (
            os.path.join(get_dev_config_dir(), "database.yml") == dev_db_config
        )

    with prod_context.resolve(db_config) as prod_db_config:
        assert (
            os.path.join(get_prod_config_dir(), "database.yml")
            == prod_db_config
        )


def test_autowire_multiple():
    @resource.create
    @impl.plain
    def foo():
        return "foo"

    @resource.create
    @impl.plain
    def bar():
        return "bar"

    @resource.create
    @impl.autowired("foo", foo)
    @impl.autowired("bar", bar)
    @impl.plain
    def baz(foo, bar):
        return "{}-{}-baz".format(foo, bar)

    context = Context()
    with context.resolve(baz) as value:
        assert "foo-bar-baz" == value
