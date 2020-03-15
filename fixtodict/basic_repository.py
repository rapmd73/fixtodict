from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from utils import version_from_xml_attrs

TYPOS = {
    "messsage": "message",
    "preceeding": "preceding",
    "Execption": "Exception",
    "ommitted": "omitted",
    "insrument": "istrument",
    "approriate": "appropriate",
    "Undelying": "undelying",
    "explaination": "explanation",
    "specifed": "specified",
    "mesage": "message",
    "Comission": "Commission",
    "positon": "position",
    "Amout": "Amount",
}

# HELPERS
# -------


def xml_get_history(root: Element, replaced=False):
    data = {}
    data["added"] = version_from_xml_attrs(root.attrib)
    data["updated"] = version_from_xml_attrs(root.attrib, prefix="updated")
    data["deprecated"] = version_from_xml_attrs(
        root.attrib, prefix="deprecated")
    if replaced:
        data["replaced"] = version_from_xml_attrs(
            root.attrib, prefix="replaced")
        if root.get("ReplacedByField") is not None:
            data["replacement"] = root.get("ReplacedByField")
    if root.get("issue"):
        data["issues"] = [root.get("issue")]
    return data


def xml_get_description(root: Element, body=False, usage=False, volume=False, elaboration=False, examples=False):
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
    return data


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
    return xml_to_sorted_dict(root, xml_to_section)


def xml_to_components(root: Element):
    return xml_to_sorted_dict(root, xml_to_component)


def xml_to_datatypes(root: Element):
    return xml_to_sorted_dict(root, xml_to_datatype)


def xml_to_fields(root: Element):
    return xml_to_sorted_dict(root, xml_to_field)


def xml_to_messages(root: Element):
    return xml_to_sorted_dict(root, xml_to_message)


def xml_to_abbreviation(root: Element):
    return (root.find("AbbrTerm").text, {
        "term": root.findtext("Term") or root.get("Term"),
        "description": xml_get_description(root, usage=True),
        "history": xml_get_history(root),
    })


def xml_to_category(root: Element):
    return (root.findtext("CategoryID"), {
        "kind": xml_get_component_type(root),
        "section": root.findtext("SectionID"),
        "fixml": {
            "filename": root.find("FIXMLFileName").text,
            "generateImpl": root.find("GenerateImplFile").text,
            "optional": bool(int(root.find("NotReqXML").text)),
        },
        "description": xml_get_description(root, body=True, volume=True),
        "history": xml_get_history(root),
    })


def xml_to_component(root: Element):
    kind = root.findtext("ComponentType")
    return (root.findtext("ComponentID") or root.get("ComponentID"), {
        "name": root.findtext("Name"),
        "nameAbbr": root.findtext("NameAbbr"),
        "kind": kind.lower() if kind else None,
        "category": root.findtext("CategoryID"),
        "description": xml_get_description(root, body=True, elaboration=True),
        "history": xml_get_history(root),
    })


def xml_to_message(root: Element):
    return (root.find("MsgType").text, {
        "name": root.find("Name").text,
        "component": root.find("ComponentID").text,
        "category": root.find("CategoryID").text,
        "section": root.find("SectionID").text,
        "fixml": {
            "optional": bool(int(root.findtext("NotReqXML"))),
        },
        "description": xml_get_description(root, body=True, elaboration=True),
        "history": xml_get_history(root),
    })


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
    return (root.find("Name").text, {
        "base": root.findtext("BaseType") or root.find("Name").text,
        "description": xml_get_description(root),
        "history": xml_get_history(root),
    })


def xml_to_section(root: Element):
    return (root.findtext("SectionID"), {
        "name": root.findtext("Name"),
        "displayOrder": root.findtext("DisplayOrder"),
        "fixml": {
            "optional": bool(int(root.findtext("NotReqXML"))),
            "filename": root.findtext("FIXMLFileName"),
        },
        "description": xml_get_description(root, volume=True, body=True),
        "history": xml_get_history(root),
    })


def xml_to_field(root: Element):
    return (root.findtext("Tag"), {
        "name": root.findtext("Name"),
        "datatype": root.findtext("Type"),
        "enum": root.findtext("EnumDatatype"),
        "description": xml_get_description(root, body=True, elaboration=True),
        "history": xml_get_history(root),
    })


def xml_to_enum(root: Element):
    return {
        "parent": root.find("Tag").text,
        "name": root.find("SymbolicName").text,
        "value": root.find("Value").text,
        "history": xml_get_history(root),
        "description": xml_get_description(root),
    }
