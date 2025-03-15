import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from be_task_ca.config import use_in_memory_repositories, use_sql_repositories
from be_task_ca.infrastructure.database.config import Base

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://postgres:example@localhost:5432/postgres_test"
)


def ensure_test_database_exists():
    """Create the test database if it doesn't exist."""
    db_name = TEST_DATABASE_URL.split('/')[-1]
    default_connection_string = TEST_DATABASE_URL.rsplit('/', 1)[0] + '/postgres'

    conn = psycopg2.connect(default_connection_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Created test database: {db_name}")

    conn.close()


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    ensure_test_database_exists()

    engine = create_engine(TEST_DATABASE_URL, poolclass=NullPool)

    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    """Create a new database session for a test."""
    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def use_sql_db():
    """Switch to SQL repositories for tests."""
    prev_type = os.environ.get("REPOSITORY_TYPE")
    use_sql_repositories()
    yield
    if prev_type:
        os.environ["REPOSITORY_TYPE"] = prev_type
    else:
        use_in_memory_repositories()


@pytest.fixture
def use_memory_db():
    """Switch to in-memory repositories for tests."""
    prev_type = os.environ.get("REPOSITORY_TYPE")
    use_in_memory_repositories()
    yield
    if prev_type:
        os.environ["REPOSITORY_TYPE"] = prev_type
    else:
        use_sql_repositories()