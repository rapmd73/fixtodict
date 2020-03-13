from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from utils import version_from_xml_attrs


def xml_get_history(root: Element, is_field=False):
    data = {"added": None, "updated": None, "deprecated": None, "issues": []}
    data["added"] = version_from_xml_attrs(root.attrib)
    data["updated"] = version_from_xml_attrs(root.attrib, prefix="updated")
    data["deprecated"] = version_from_xml_attrs(
        root.attrib, prefix="deprecated")
    if root.get("issue"):
        data["issues"].append(root.get("issue"))
    if is_field:
        data["replaced"] = version_from_xml_attrs(
            root.attrib, prefix="replaced")
        if root.get("ReplacedByField") is not None:
            data["replacement"] = root.get("ReplacedByField")
    return data


def xml_get_description(root: Element, volume=False, elaboration=False):
    data = {"paragraphs": [], "usage": None, "examples": []}
    for child in root.findall("Description"):
        data["paragraphs"].append(child.text)
    if root.find("Usage") is not None:
        data["usage"] = root.find("Usage").text
    if volume:
        data["volume"] = None
        if root.find("Volume") is not None:
            data["volume"] = root.find("Volume").text
    if elaboration:
        data["elaboration"] = None
        if root.find("Elaboration") is not None:
            data["elaboration"] = root.find("Elaboration").text
    for child in root.findall("Example"):
        data["examples"].append(child.text)
    return data


def xml_get_component_type(root: Element):
    return str.lower(root.find("ComponentType").text)


def xml_to_abbreviations(root: Element):
    return [xml_to_abbreviation(c) for c in root]


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
    data = {}
    for child in root:
        data.update(xml_to_category(child))
    return data


def xml_to_msg_contents(root: Element):
    return [xml_to_msg_content(c) for c in root]


def xml_to_sections(root: Element):
    data = {}
    for child in root:
        data.update(xml_to_section(child))
    return data


def xml_to_components(root: Element):
    data = {}
    for child in root:
        data.update(xml_to_component(child))
    return data


def xml_to_datatypes(root: Element):
    data = {}
    for child in root:
        data.update(xml_to_datatype(child))
    return data


def xml_to_fields(root: Element):
    data = {}
    for child in root:
        data.update(xml_to_field(child))
    return data


def xml_to_messages(root: Element):
    data = {}
    for child in root:
        data.update(xml_to_message(child))
    return data


def xml_to_abbreviation(root: Element):
    name = root.find("AbbrTerm").text
    data = {}
    data["term"] = root.find("Term").text
    data["description"] = xml_get_description(root)
    data["history"] = xml_get_history(root)
    return {name: data}


def xml_to_category(root: Element):
    cat_id = root.find("CategoryID").text
    data = {}
    data["kind"] = xml_get_component_type(root)
    data["section"] = None
    if root.find("SectionID") is not None:
        data["section"] = root.find("SectionID").text
    data["fixml"] = {}
    if root.find("FIXMLFileName") is not None:
        data["fixml"]["filename"] = root.find("FIXMLFileName").text
    if root.find("GenerateImplFile") is not None:
        data["fixml"]["generate"] = bool(
            int(root.find("GenerateImplFile").text))
    if root.find("NotReqXML") is not None:
        data["fixml"]["optional"] = bool(int(root.find("NotReqXML").text))
    data["description"] = xml_get_description(root, volume=True)
    data["history"] = xml_get_history(root)
    return {cat_id: data}


def xml_to_component(root: Element):
    comp_id = root.find("ComponentID").text
    data = {}
    data["name"] = root.find("Name").text
    data["kind"] = str.lower(root.find("ComponentType").text)
    data["category"] = root.find("CategoryID").text
    return {comp_id: data}


def xml_to_message(root: Element):
    msg_id = root.find("MsgType").text
    data = {}
    data["name"] = root.find("Name").text
    data["category"] = root.find("CategoryID").text
    data["section"] = root.find("SectionID").text
    data["fixml"] = {}
    if root.find("NotReqXML") is not None:
        data["fixml"]["optional"] = bool(int(root.find("NotReqXML").text))
    data["description"] = xml_get_description(root)
    data["history"] = xml_get_history(root)
    return {msg_id: data}


def xml_to_msg_content(root: Element):
    data = {}
    data["parent"] = root.find("ComponentID").text
    data["tag"] = root.find("TagText").text
    data["i"] = float(root.find("Position").text)
    data["optional"] = not bool(int(root.find("Reqd").text))
    data["description"] = xml_get_description(root)
    data["history"] = xml_get_history(root)
    return data


def xml_to_datatype(root: Element):
    name = root.find("Name").text
    data = {}
    if root.find("BaseType") is not None:
        data["baseDatatype"] = root.find("BaseType").text
    data["description"] = xml_get_description(root)
    data["history"] = xml_get_history(root)
    return {name: data}


def xml_to_section(root: Element):
    sect_id = root.find("SectionID").text
    data = {}
    if root.find("Name") is not None:
        data["name"] = root.find("Name").text
    if root.find("Volume") is not None:
        data["volume"] = root.find("Volume").text
    if root.find("DisplayOrder") is not None:
        data["displayOrder"] = root.find("DisplayOrder").text
    if root.find("FIXMLFileName") is not None:
        data["fixml"] = {}
        data["fixml"]["filename"] = root.find("FIXMLFileName").text
    return {sect_id: data}


def xml_to_field(root: Element):
    data = {}
    data["name"] = root.find("Name").text
    data["datatype"] = root.find("Type").text
    if root.find("EnumDatatype") is not None:
        data["enum"] = root.find("EnumDatatype").text
    data["history"] = xml_get_history(root, is_field=True)
    data["description"] = xml_get_description(root, elaboration=True)
    return {root.find("Tag").text: data}


def xml_to_enum(root: Element):
    data = {}
    data["parent"] = root.find("Tag").text
    data["name"] = root.find("SymbolicName").text
    data["value"] = root.find("Value").text
    data["history"] = xml_get_history(root, is_field=True)
    data["description"] = xml_get_description(root, elaboration=True)
    return data
