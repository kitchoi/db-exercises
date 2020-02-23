import os
import shutil
import tempfile

from sqlalchemy import create_engine


def setup_sqlite_engine(test_case):
    temp_folder = tempfile.mkdtemp()
    test_case.addCleanup(shutil.rmtree, temp_folder)
    db = os.path.join(temp_folder, "test.db")
    url = "sqlite:////{}".format(db)
    engine = create_engine(url)
    return engine


def setup_postgres_engine(test_case):
    url = os.environ["POSRGRES_URL"]
    return create_engine(url)


class SQLiteBackend:

    def setUp(self):
        self.engine = setup_sqlite_engine(self)

    def tearDown(self):
        pass


class PostgresBackend:

    def setUp(self):
        self.engine = setup_postgres_engine(self)

    def tearDown(self):
        pass


class MultiBackend:

    def setUp(self):
        self.sqlite_engine = setup_sqlite_engine(self)
        self.postgres_engine = setup_postgres_engine(self)

    def tearDown(self):
        pass

    def engines(self):
        yield self.sqlite_engine
        yield self.postgres_engine
