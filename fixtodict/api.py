import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from typing import Optional, Dict
import sys

from .basic_repository import (xml_to_abbreviations, xml_to_categories,
                               xml_to_components, xml_to_msg_contents,
                               xml_to_enums, xml_to_datatypes, xml_to_fields,
                               xml_to_messages, xml_to_sections)
from .utils import iso8601_local, target_filename, parse_protocol_version
from .version import __version__

LEGAL_INFO = 'FIXtodict is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'


def fixipe_dictionary_link(version):
    return "https://fixipe.com/#/explore/{fix}/{major}.{minor}/servicepack/{sp}".format(
        **version)


def xml_files_to_fix_dict(xml_files: Dict[str, Optional[Element]]):
    # `xml_files["fields"]` is incorrect in FIX 4.3.
    version = parse_protocol_version(xml_files["messages"].get("version"))
    abbreviations = xml_to_abbreviations(xml_files["abbreviations"])
    datatypes = xml_to_datatypes(xml_files["datatypes"])
    sections = xml_to_sections(xml_files["sections"])
    categories = xml_to_categories(xml_files["categories"])
    fields = xml_to_fields(xml_files["fields"])
    components = xml_to_components(xml_files["components"])
    messages = xml_to_messages(xml_files["messages"])
    enums = xml_to_enums(xml_files["enums"])
    msg_contents = xml_to_msg_contents(xml_files["msg_contents"])
    # Embed stuff.
    for value in fields.values():
        if value["name"] == "RefMsgType":
            print("-- Handling special case for `RefMsgType(372)`.")
            del value["enum"]
        elif value["enum"] is not None:
            value["enum"] = enums[value["enum"]]
    for elements in msg_contents.values():
        for elem in elements:
            if elem["tag"] not in fields:
                for c in components.values():
                    if c["name"] == elem["tag"]:
                        elem["kind"] = "component"
                        break
            else:
                elem["kind"] = "field"
    for value in messages.values():
        value["breakdown"] = msg_contents[value["component"]]
        del value["component"]
    for (key, value) in components.items():
        # Check this on online FIX Dictionary.
        if key not in msg_contents:
            msg_contents[key] = []
        value["breakdown"] = msg_contents[key]
    return {
        "fixtodict": {
            "version": __version__,
            "legal": LEGAL_INFO,
            "md5": "",
            "command": " ".join(sys.argv),
            "generated": iso8601_local(),
            "fixipe": fixipe_dictionary_link(version),
        },
        "version": version,
        "copyright": "Copyright (c) FIX Protocol Limited, all rights reserved",
        "abbreviations": abbreviations,
        "datatypes": datatypes,
        "sections": sections,
        "categories": categories,
        "fields": fields,
        "components": components,
        "messages": messages,
    }
