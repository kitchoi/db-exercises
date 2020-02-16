import unittest

from project import orm


class TestORM(unittest.TestCase):

    def test_bases(self):
        # Check all tables are defined properly
        self.assertIsNotNone(orm.Base.metadata)

