import unittest
import os
from ..basic_repository import *
from ..resources import test_cases


class TestBasicRepository(unittest.TestCase):

    def test_abbreviation(self):
        for (original, expected) in test_cases("abbreviations"):
            self.assertEqual(xml_to_abbreviation(original), tuple(expected))

    def test_datatypes(self):
        pass

    def test_fields(self):
        pass
