import sys
from xml.etree.ElementTree import Element
from typing import Optional, Dict

from .utils import (
    iso8601_local,
    parse_protocol_version,
    filter_none,
    version_from_xml_attrs,
)
from .resources import LEGAL_INFO
from .__version__ import __version__

FILENAME_ABBREVIATIONS = "Abbreviations.xml"
FILENAME_CATEGORIES = "Categories.xml"
FILENAME_COMPONENTS = "Components.xml"
FILENAME_DATATYPES = "Datatypes.xml"
FILENAME_ENUMS = "Enums.xml"
FILENAME_FIELDS = "Fields.xml"
FILENAME_MESSAGES = "Messages.xml"
FILENAME_MSG_CONTENTS = "MsgContents.xml"
FILENAME_SECTIONS = "Sections.xml"

# HELPERS
# -------


def xml_get_history(root: Element, replaced=False):
    data = {}
    data["added"] = version_from_xml_attrs(root.attrib)
    data["updated"] = version_from_xml_attrs(root.attrib, prefix="updated")
    data["deprecated"] = version_from_xml_attrs(
        root.attrib, prefix="deprecated"
    )
    if replaced:
        data["replaced"] = version_from_xml_attrs(
            root.attrib, prefix="replaced"
        )
        if root.get("ReplacedByField") is not None:
            data["replacement"] = root.get("ReplacedByField")
    if root.get("issue"):
        data["issues"] = [root.get("issue")]
    return filter_none(data)


def xml_get_description(
    root: Element,
    body=False,
    usage=False,
    volume=False,
    elaboration=False,
    examples=False,
):
    data = {}
    if body:
        data["body"] = root.findtext("Description")
    if usage:
        data["usage"] = root.findtext("Usage")
    if volume:
        data["volume"] = root.findtext("Volume")
    if elaboration:
        data["elaboration"] = root.findtext("Elaboration")
    if examples:
        data["examples"] = [c.text for c in root.findall("Example")]
    return filter_none(data)


def xml_get_component_type(root: Element):
    return str.lower(root.find("ComponentType").text)


# MAIN XML EXPLORERS
# ------------------


def xml_to_sorted_dict(root: Element, f):
    if root is None:
        root = []
    data = sorted([f(c) for c in root], key=lambda x: str.lower(x[0]))
    return {k: v for (k, v) in data}


def xml_to_abbreviations(root: Element):
    return xml_to_sorted_dict(root, xml_to_abbreviation)


def xml_to_enums(root: Element):
    data = {}
    for child in root:
        enum = xml_to_enum(child)
        parent = enum["parent"]
        if parent not in data:
            data[parent] = []
        del enum["parent"]
        data[parent].append(enum)
    return data


def xml_to_categories(root: Element):
    return xml_to_sorted_dict(root, xml_to_category)


def xml_to_msg_contents(root: Element):
    data = {}
    for child in root:
        elem = xml_to_msg_content(child)
        parent = elem["parent"]
        if parent not in data:
            data[parent] = []
        data[parent].append(elem)
    return {k: sorted(v, key=lambda x: x["i"]) for (k, v) in data.items()}


def xml_to_sections(root: Element):
    if root is None:
        root = []
    data = [xml_to_section(c) for c in root]
    return {k: v for (k, v) in data}


def xml_to_components(root: Element):
    return xml_to_sorted_dict(root, xml_to_component)


def xml_to_datatypes(root: Element):
    if root is None:
        root = []
    data = [xml_to_datatype(c) for c in root]
    return {k: v for (k, v) in data}


def xml_to_fields(root: Element):
    return xml_to_sorted_dict(root, xml_to_field)


def xml_to_messages(root: Element):
    return xml_to_sorted_dict(root, xml_to_message)


def xml_to_abbreviation(root: Element):
    return (
        root.find("AbbrTerm").text,
        {
            "term": root.findtext("Term") or root.get("Term"),
            "description": xml_get_description(root, usage=True),
            "history": xml_get_history(root),
        },
    )


def xml_to_category(root: Element):
    return (
        root.findtext("CategoryID"),
        {
            "kind": xml_get_component_type(root),
            "section": root.findtext("SectionID"),
            "fixml": {
                "filename": root.find("FIXMLFileName").text,
                "generateImpl": root.find("GenerateImplFile").text,
                "optional": bool(int(root.find("NotReqXML").text)),
            },
            "description": xml_get_description(root, body=True, volume=True),
            "history": xml_get_history(root),
        },
    )


def xml_to_component(root: Element):
    kind = root.findtext("ComponentType")
    return (
        root.findtext("ComponentID") or root.get("ComponentID"),
        {
            "name": root.findtext("Name"),
            "nameAbbr": root.findtext("NameAbbr"),
            "kind": kind.lower() if kind else None,
            "category": root.findtext("CategoryID"),
            "description": xml_get_description(
                root, body=True, elaboration=True
            ),
            "history": xml_get_history(root),
        },
    )


def xml_to_message(root: Element):
    return (
        root.find("MsgType").text,
        {
            "name": root.find("Name").text,
            "component": root.find("ComponentID").text,
            "category": root.find("CategoryID").text,
            "section": root.find("SectionID").text,
            "fixml": {"optional": bool(int(root.findtext("NotReqXML"))),},
            "description": xml_get_description(
                root, body=True, elaboration=True
            ),
            "history": xml_get_history(root),
        },
    )


def xml_to_msg_content(root: Element):
    return {
        "parent": root.find("ComponentID").text,
        "tag": root.find("TagText").text,
        "kind": None,
        "i": float(root.find("Position").text),
        "optional": not bool(int(root.find("Reqd").text)),
        "inlined": bool(int(root.findtext("Inlined", default="1"))),
        "description": xml_get_description(root, body=True),
        "history": xml_get_history(root),
    }


def xml_to_datatype(root: Element):
    return (
        root.find("Name").text,
        {
            "base": root.findtext("BaseType") or root.find("Name").text,
            "description": xml_get_description(root, examples=True, body=True),
            "history": xml_get_history(root),
        },
    )


def xml_to_section(root: Element):
    return (
        root.findtext("SectionID"),
        {
            "name": root.findtext("Name"),
            "fixml": {
                "optional": bool(int(root.findtext("NotReqXML"))),
                "filename": root.findtext("FIXMLFileName"),
            },
            "description": xml_get_description(root, volume=True, body=True),
            "history": xml_get_history(root),
        },
    )


def xml_to_field(root: Element):
    return (
        root.findtext("Tag"),
        {
            "name": root.findtext("Name"),
            "datatype": root.findtext("Type"),
            "enum": root.findtext("EnumDatatype"),
            "description": xml_get_description(
                root, body=True, elaboration=True
            ),
            "history": xml_get_history(root),
        },
    )


def xml_to_enum(root: Element):
    return {
        "parent": root.find("Tag").text,
        "name": root.find("SymbolicName").text,
        "value": root.find("Value").text,
        "history": xml_get_history(root),
        "description": xml_get_description(root),
    }


def xml_files_to_repository(xml_files: Dict[str, Optional[Element]]):
    # `xml_files["fields"]` is incorrect in FIX 4.3.
    version = parse_protocol_version(xml_files["Messages.xml"].get("version"))
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
        "meta": {
            "version": version,
            "fixtodict": {
                "version": __version__,
                "legal": LEGAL_INFO,
                "md5": "",
                "command": " ".join(sys.argv),
                "timestamp": iso8601_local(),
            },
        },
        "copyright": "Copyright (c) FIX Protocol Limited, all rights reserved",
        "abbreviations": abbreviations,
        "datatypes": datatypes,
        "sections": sections,
        "categories": categories,
        "fields": fields,
        "components": components,
        "messages": messages,
    }
