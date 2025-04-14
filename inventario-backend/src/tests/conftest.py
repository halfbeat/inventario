# pylint: disable=redefined-outer-name

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from tenacity import retry, stop_after_delay


pytest.register_assert_rewrite("tests.e2e.api_client")


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    # metadata.create_all(engine)
    return engine

@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture
def mappers():
    # start_mappers()
    yield
    clear_mappers()


@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(engine):
    return engine.connect()


# @retry(stop=stop_after_delay(10))
# def wait_for_webapp_to_come_up():
#     return requests.get(config.get_api_url())


# @pytest.fixture
# def restart_api():
#     (Path(__file__).parent / "../src/allocation/entrypoints/flask_app.py").touch()
#     time.sleep(0.5)
#     wait_for_webapp_to_come_up()
