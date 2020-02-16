import os
import shutil
import tempfile
import unittest

from sqlalchemy import create_engine

from project import actions


class SQLiteMixin:

    def setUp(self):
        temp_folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, temp_folder)
        db = os.path.join(temp_folder, "test.db")
        self.url = "sqlite:////{}".format(db)

    def tearDown(self):
        pass


class PostgresMixin:

    def setUp(self):
        self.url = "postgresql://postgres:postgres@0.0.0.0/testdb"

    def tearDown(self):
        pass


class CheckActionMixin:

    def setUp(self):
        self.backend.setUp(self)
        self.engine = create_engine(self.url)
        actions.populate_db(self.url, reset=True)

    def tearDown(self):
        self.engine.dispose()
        self.backend.tearDown(self)

    def test_populate_db(self):
        self.assertGreater(actions.count_managers(self.engine), 0)

    def test_get_manager_by_name(self):
        manager = actions.get_manager_by_name(self.engine, "Adam")
        self.assertEqual(manager.name, "Adam")

    def test_get_manager_by_venue_like(self):
        managers = actions.get_manager_by_venue_like(
            self.engine,
            patterns=["Garden", "%Hall"]
        )
        self.assertEqual(
            sorted(m.name for m in managers),
            ["Adam", "Eve"]
        )

        managers = actions.get_manager_by_venue_like(
            self.engine,
            patterns=["%Hall"]
        )
        self.assertEqual(
            sorted(m.name for m in managers),
            ["Adam"],
        )

    def test_get_all_venue_names(self):
        names = actions.get_all_venue_names(self.engine)
        self.assertEqual(len(names), 5)
        self.assertIn("Library", names)

    def test_get_venue_name_match_any(self):
        names = actions.get_venue_name_match_any(
            self.engine, patterns=["%Hall", "%Garden"])
        self.assertEqual(
            names,
            [
                "Dancing Hall",
                "Dining Hall",
                "Garden",
                "Pool Garden",
            ]
        )


class TestActionSQLite(CheckActionMixin, SQLiteMixin, unittest.TestCase):

    backend = SQLiteMixin


class TestActionPostgres(CheckActionMixin, PostgresMixin, unittest.TestCase):

    backend = PostgresMixin
