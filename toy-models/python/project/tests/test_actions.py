import datetime
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

    def test_get_events_by_date_range(self):
        events = actions.get_events_by_date_range(
            engine=self.engine,
            start_date=datetime.date(2018, 8, 1),
            end_date=datetime.date(2019, 1, 1),
        )

        self.assertEqual(len(events), 2)
        event_names = sorted(e.name for e in events)
        self.assertEqual(event_names, ["Comic Con", "Medical conference"])

    def test_get_events_in_venue(self):
        events = actions.get_events_in_venue(
            engine=self.engine,
            venue_name="Library",
        )
        self.assertEqual(len(events), 2)
        event_names = sorted(e.name for e in events)
        self.assertEqual(event_names, ["Bible study", "Medical conference"])


class TestActionSQLite(CheckActionMixin, SQLiteMixin, unittest.TestCase):

    backend = SQLiteMixin


class TestActionPostgres(CheckActionMixin, PostgresMixin, unittest.TestCase):

    backend = PostgresMixin
