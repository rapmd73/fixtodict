from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from .utils import protocol_from_xml_attrs


def xml_to_datatypes(root: Element):
    data = {}
    for child in root:
        name = child.get("name")
        data[name] = {}
        base_datatype = child.get("baseType")
        if base_datatype:
            data[name]["baseDatatype"] = base_datatype
        data[name]["description"] = child.get("text")
        xml_details = child.find("XML")
        if xml_details is not None:
            data[name]["xmlBaseDatatype"] = xml_details.get("base")
            data[name]["xmlBuiltIn"] = xml_details.get("builtin") == "1"
            data[name]["xmlDescription"] = child.get("text")
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def xml_to_sections(root: Optional[Element]):
    if root is None:
        return {}
    data = {}
    for child in sorted(root, key=lambda c: c.get("id")):
        name = child.get("id")
        data[name] = {}
        data[name]["description"] = child.get("text")
    return data


def xml_to_categories(root: Optional[Element]):
    if root is None:
        return {}
    data = {}
    for child in sorted(root, key=lambda c: c.get("id")):
        name = child.get("id")
        data[name] = {}
        data[name]["section"] = child.get("section")
        data[name]["volume"] = child.get("volume")
    return data


def xml_to_abbreviations(root: Optional[Element]):
    if root is None:
        return {}
    data = {}
    for child in sorted(root, key=lambda c: c.get("abbrTerm")):
        name = child.get("abbrTerm")
        data[name] = {}
        # "usage" attribute doesn't seem used at all, so let's ignore it.
        data[name]["term"] = child.get("text")
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def xml_to_fields(root: Element):
    data = {}
    for child in sorted(root, key=lambda c: int(c.get("id"))):
        name = child.get("name")
        data[name] = {}
        data[name]["id"] = child.get("id")
        data[name]["description"] = child.get("text")
        data[name]["datatype"] = child.get("type")
        data[name]["enums"] = child.get("type")
        if len(child) > 0:
            data[name]["enums"] = {}
        for subchild in child:
            val = subchild.get("value")
            data[name]["enums"][val] = {}
            e = data[name]["enums"][val]
            e["name"] = subchild.get("symbolicName")
            e["description"] = subchild.get("text")
            e["added"] = protocol_from_xml_attrs({
                **child.attrib,
                **subchild.attrib
            })
        try:
            data[name]["requiredFixml"] = child.get("notReqXML") == "0"
        except:
            pass
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def xml_to_components(root: Element):
    data = {}
    for child in sorted(root, key=lambda c: int(c.get("id"))):
        name = child.get("name")
        data[name] = {}
        data[name]["id"] = child.get("id")
        data[name]["name"] = child.get("name")
        data[name]["category"] = child.get("category")
        data[name]["kind"] = child.get("type")
        data[name]["isRepeating"] = child.get("repeating") == "1"
        data[name]["description"] = child.get("text")
        data[name]["contents"] = xml_to_message_entities(child)
        try:
            data[name]["requiredFixml"] = item["@notReqXML"] == "0"
        except:
            pass
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def xml_to_messages(root: Element):
    data = {}
    for child in sorted(root, key=lambda c: int(c.get("id"))):
        name = child.get("name")
        data = {}
        data[name] = {}
        data[name]["id"] = child.get("id")
        data[name]["category"] = child.get("category")
        data[name]["section"] = child.get("section")
        data[name]["contents"] = xml_to_message_entities(child)
        data[name]["requiredFixml"] = child.get("notReqXML") == "0"
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def xml_to_message_entities(root: Element):
    data = []
    i = 0
    for child in root:
        data.append({})
        data[i]["id"] = child.get("id")
        data[i]["name"] = child.get("name")
        data[i]["kind"] = "field" if child.tag == "fieldRef" else "component"
        data[i]["required"] = child.get("required") == "1"
        data[i]["description"] = child.get("text")
        i += 1
    return data
