import pytest
from challenge_halo.app import create_app
from challenge_halo.redis_utils import RedisUtils
from challenge_halo.routes import configure_routes


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    configure_routes(app)
    redis_utilities = RedisUtils()
    # Teardown process removes all redis data to ensure later tests are not influenced by previous ones
    redis_utilities.flushall()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
