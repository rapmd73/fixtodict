import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from typing import Optional, Dict
import sys

from basic_repository import (xml_to_abbreviations, xml_to_categories, xml_to_components, xml_to_msg_contents, xml_to_enums,
                              xml_to_datatypes, xml_to_fields, xml_to_messages, xml_to_sections)
from utils import iso8601_local, target_filename, parse_protocol_version
from version import __version__


LEGAL_INFO = 'FIXtodict is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'


def fixipe_dictionary_link(version):
    return "https://fixipe.com/#/explore/{fix}/{major}.{minor}/servicepack/{sp}".format(
        **version)


def xml_files_to_fix_dict(xml_files: Dict[str, Optional[Element]]):
    version = parse_protocol_version(xml_files["fields"].get("version"))
    abbreviations = xml_to_abbreviations(xml_files["abbreviations"])
    datatypes = xml_to_datatypes(xml_files["datatypes"])
    sections = xml_to_sections(xml_files["sections"])
    categories = xml_to_categories(xml_files["categories"])
    fields = xml_to_fields(xml_files["fields"])
    components = xml_to_components(xml_files["components"])
    messages = xml_to_messages(xml_files["messages"])
    enums = xml_to_enums(xml_files["enums"])
    msg_contents = xml_to_msg_contents(xml_files["msg_contents"])
    for (key, value) in fields.items():
        if "enum" in value:
            value["enum"] = enums[value["enum"]]
    return {
        "fixtodict": {
            "version": __version__,
            "legal": LEGAL_INFO,
            "command": " ".join(sys.argv),
            "generated": iso8601_local(),
            "fixipe": fixipe_dictionary_link(version)
        },
        "version": version,
        "abbreviations": abbreviations,
        "datatypes": datatypes,
        "sections": sections,
        "categories": categories,
        "fields": fields,
        "components": components,
        "messages": messages,
        "msg_contents": msg_contents,
    }
