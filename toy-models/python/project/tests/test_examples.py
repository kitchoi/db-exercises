import unittest

from project import examples
from project.testing import PostgresBackend


class TestExample(PostgresBackend, unittest.TestCase):

    def test_run_example(self):
        results = examples.run_example(self.engine)
        self.assertGreater(len(results), 0)
