from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from .utils import protocol_from_xml_attrs


def xml_to_abbreviation(root: Element):
    name = root.find("AbbrTerm").text
    data = {}
    if root.get("Term") is not None:
        data["term"] = root.get("Term")
    if root.find("Term") is not None:
        data["term"] = root.find("Term").text
    if root.find("Usage") is not None:
        data["usage"] = root.find("Usage").text
    if root.get("added") is not None:
        data["added"] = protocol_from_xml_attrs(root.attrib)
    return {name: data}


def xml_to_section(root: Element):
    sect_id = root.get("SectionID")
    data = {}
    if root.find("Name") is not None:
        data["name"] = root.find("Name").text
    if root.find("Volume") is not None:
        data["volume"] = root.find("Volume").text
    if root.find("DisplayOrder") is not None:
        data["displayOrder"] = root.find("DisplayOrder").text
    return {sect_id: data}


def xml_to_category(root: Element):
    cat_id = root.get("CategoryID")
    data = {}
    return {cat_id: data}


def xml_to_datatype(root: Element):
    name = root.find("Name").text
    data = {}
    if root.find("BaseType") is not None:
        data["baseDatatype"] = root.find("BaseType").text
    if root.find("Description") is not None:
        data["description"] = root.find("Description").text
    if root.find("Example") is not None:
        data["examples"] = []
        for e in root.findall("Example"):
            data["examples"].append(e.text)
    if root.get("added") is not None:
        data["added"] = protocol_from_xml_attrs(root.attrib)
    return {name: data}


def xml_to_field(root: Element):
    data = {}
    if root.find("Name") is not None:
        data["name"] = root.find("Name").text
    if root.find("Type") is not None:
        data["type"] = root.find("Type").text
    if root.find("Description") is not None:
        data["description"] = root.find("Description").text
    if root.find("Elaboration") is not None:
        data["elaboration"] = root.find("Elaboration").text
    return {root.get("Tag"): data}
