import unittest
from fixtodict.basic_repository_v1 import (
    xml_to_abbreviation,
    xml_to_datatype,
    xml_to_field,
)
from fixtodict.resources import test_cases


class TestBasicRepository(unittest.TestCase):
    def test_abbreviation(self):
        for (original, expected) in test_cases("abbreviations"):
            self.assertEqual(xml_to_abbreviation(original), tuple(expected))

    def test_datatypes(self):
        for (original, expected) in test_cases("datatypes"):
            self.assertEqual(xml_to_datatype(original), tuple(expected))

    def test_fields(self):
        for (original, expected) in test_cases("fields"):
            self.assertEqual(xml_to_field(original), tuple(expected))
