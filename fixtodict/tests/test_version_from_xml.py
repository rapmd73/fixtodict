import unittest
from xml.etree import ElementTree
from ..utils import version_from_xml_attrs


def xml_string_to_version(data, prefix):
    return version_from_xml_attrs(
        ElementTree.fromstring(data).attrib, prefix=prefix
    )


class TestVersionParser(unittest.TestCase):
    def test_updated_50SP1EP97(self):
        data = """
        <Message
            updated="FIX.5.0SP1"
            updatedEP="97"
            added="FIX.4.4"
            addedEP="-1">
        </Message>
        """
        self.assertEqual(
            xml_string_to_version(data, "updated"),
            {"fix": "fix", "major": "5", "minor": "0", "sp": "1", "ep": "97"},
        )

    def test_added_44(self):
        data = """
        <Component
            updated="FIX.5.0SP1"
            updatedEP="97"
            added="FIX.4.4"
            addedEP="-1">
        </Component>
        """
        self.assertEqual(
            xml_string_to_version(data, "added"),
            {"fix": "fix", "major": "4", "minor": "4", "sp": "0"},
        )
