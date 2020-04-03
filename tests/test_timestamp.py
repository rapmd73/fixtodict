import unittest
import datetime
from fixtodict.utils import iso8601_local


class TestTimestamp(unittest.TestCase):
    def test_is_valid_iso8601(self):
        datetime.datetime.strptime(iso8601_local(), "%Y-%m-%dT%H:%M:%SZ")
