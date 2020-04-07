import unittest
from fixtodict.xml_logic import (
    xml_to_datatype,
)
from fixtodict.resources import test_cases


class TestElemDatatype(unittest.TestCase):
    def test_expected(self):
        for (original, expected) in test_cases("datatypes"):
            self.assertEqual(
                xml_to_datatype(original), tuple(expected))
