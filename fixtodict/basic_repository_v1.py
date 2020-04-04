import sys
from xml.etree.ElementTree import Element

from .utils import (
    iso8601_utc,
    filter_none,
)
from .fix_version import FixVersion
from .resources import LEGAL_INFO
from .__version__ import __version__


def transform_basic_repository_v1(
    abbreviations: Element,
    categories: Element,
    components: Element,
    datatypes: Element,
    enums: Element,
    fields: Element,
    messages: Element,
    msg_contents: Element,
    sections: Element,
):
    fix_version = FixVersion(messages.get("version")).data
    abbreviations = xml_to_abbreviations(abbreviations)
    categories = xml_to_categories(categories)
    components = xml_to_components(components)
    datatypes = xml_to_datatypes(datatypes)
    enums = xml_to_enums(enums)
    fields = xml_to_fields(fields)
    messages = xml_to_messages(messages)
    msg_contents = xml_to_msg_contents(msg_contents)
    sections = xml_to_sections(sections)
    # Embed enums into fields.
    for value in fields.values():
        # Handling special case for `RefMsgType(372)`.
        if value["name"] == "RefMsgType":
            del value["enum"]
        elif "enum" in value:
            value["enum"] = enums[value["enum"]]
    # Check the kind of content inside messages.
    for elements in msg_contents.values():
        for elem in elements:
            if elem["tag"] not in fields:
                for c in components.values():
                    if c["name"] == elem["tag"]:
                        elem["kind"] = "component"
                        break
            else:
                elem["kind"] = "field"
    # Embed contents into messages.
    for value in messages.values():
        value["breakdown"] = msg_contents[value["component"]]
        del value["component"]
    # Embed contents into components.
    for (key, value) in components.items():
        # TODO: check affected components on FIX Dictionary.
        if key not in msg_contents:
            msg_contents[key] = []
        value["breakdown"] = msg_contents[key]
    return {
        "meta": {
            "schema": "1",
            "version": fix_version,
            "copyright": "Copyright (c) FIX Protocol Limited, all rights reserved",
            "fixtodict": {
                "version": __version__,
                "legal": LEGAL_INFO,
                "md5": "",
                "command": " ".join(sys.argv),
                "timestamp": iso8601_utc(),
            },
        },
        "abbreviations": abbreviations,
        "datatypes": datatypes,
        "sections": sections,
        "categories": categories,
        "fields": fields,
        "components": components,
        "messages": messages,
    }


# HELPERS
# -------


def xml_get_history(root: Element, replaced=False):
    data = {}
    keywords = ["added", "updated", "deprecated"]
    if replaced:
        keywords.append("replaced")
        if root.get("ReplacedByField") is not None:
            data["replacement"] = root.get("ReplacedByField")
    for keyword in keywords:
        version = FixVersion.create_from_xml_attrs(root.attrib, keyword)
        if version is not None:
            data[keyword] = version.data
    if root.get("issue"):
        data["issues"] = [root.get("issue")]
    return filter_none(data)


def xml_get_docs(
    root: Element,
    body=False,
    usage=False,
    volume=False,
    elaboration=False,
    examples=False,
):
    data = {}
    if body:
        data["description"] = root.findtext("Description")
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
    return {
        k: sorted(v, key=lambda x: x["position"]) for (k, v) in data.items()
    }


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
            "docs": xml_get_docs(root, usage=True),
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
            "docs": xml_get_docs(root, body=True, volume=True),
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
            "docs": xml_get_docs(root, body=True, elaboration=True),
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
            "fixml": {"optional": bool(int(root.findtext("NotReqXML")))},
            "docs": xml_get_docs(root, body=True, elaboration=True),
            "history": xml_get_history(root),
        },
    )


def xml_to_msg_content(root: Element):
    return {
        "parent": root.find("ComponentID").text,
        "tag": root.find("TagText").text,
        "kind": None,
        "position": float(root.find("Position").text),
        "optional": not bool(int(root.find("Reqd").text)),
        "inlined": bool(int(root.findtext("Inlined", default="1"))),
        "docs": xml_get_docs(root, body=True),
        "history": xml_get_history(root),
    }


def xml_to_datatype(root: Element):
    return (
        root.get("Name") or root.find("Name").text,
        filter_none(
            {
                "base": root.findtext("Base"),
                "docs": xml_get_docs(root, examples=True, body=True),
                "history": xml_get_history(root),
            }
        ),
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
            "docs": xml_get_docs(root, volume=True, body=True),
            "history": xml_get_history(root),
        },
    )


def xml_to_field(root: Element):
    return (
        root.findtext("Tag") or root.get("Tag"),
        filter_none(
            {
                "name": root.findtext("Name"),
                "datatype": root.findtext("Type"),
                "enum": root.findtext("EnumDatatype"),
                "docs": xml_get_docs(root, body=True, elaboration=True),
                "history": xml_get_history(root),
            }
        ),
    )


def xml_to_enum(root: Element):
    return {
        "parent": root.find("Tag").text,
        "name": root.find("SymbolicName").text,
        "value": root.find("Value").text,
        "history": xml_get_history(root),
        "docs": xml_get_docs(root),
    }
