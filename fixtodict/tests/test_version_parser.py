import unittest
from ..utils import parse_protocol_version


class TestVersionParser(unittest.TestCase):
    def test_40(self):
        self.assertEqual(
            parse_protocol_version("fix.4.0"),
            {"fix": "fix", "major": "4", "minor": "0", "sp": "0"},
        )

    def test_50SP2EP254(self):
        self.assertEqual(
            parse_protocol_version("fix.5.0SP2", ep="254"),
            {"fix": "fix", "major": "5", "minor": "0", "sp": "2", "ep": "254"},
        )

    def test_fixt_11(self):
        self.assertEqual(
            parse_protocol_version("fixt.1.1"),
            {"fix": "fixt", "major": "1", "minor": "1", "sp": "0"},
        )
