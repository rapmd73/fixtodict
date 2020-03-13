from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from repo_basic import xml_to_abbreviation, xml_to_category, xml_to_datatype, xml_to_field, xml_to_section


def apply_extension_pack(original, changes):
    for new_abbr in changes["abbreviations"]["+"]:
        original["abbreviations"].update(new_abbr)


def extension_pack_from_path(path):
    xml = ElementTree.parse(path).getroot()[0]
    return xml_to_extension_pack(xml)


def xml_to_extension_pack(root: Element):
    data = {}
    data["id"] = root.get("id")
    data["approved"] = root.get("approved")
    data["description"] = root.get("desc")
    data["changes"] = {}
    data["changes"]["inserts"] = {}
    data["changes"]["deletes"] = {}
    data["changes"]["deprecations"] = {}
    data["changes"]["updates"] = {}
    resource_kinds = [
        ["abbreviations", "Abbreviations", "Abbreviation", xml_to_abbreviation],
        ["components", "Components", "Component", xml_to_abbreviation],  # FIXME
        ["datatypes", "Datatypes", "Datatype", xml_to_datatype],
        ["fields", "Fields", "Field", xml_to_field],
        ["categories", "Categories", "Category", xml_to_category],
        ["sections", "Sections", "Section", xml_to_section],
    ]
    for resource_kind in resource_kinds:
        data["changes"]["inserts"][resource_kind[0]] = {}
        data["changes"]["deletes"][resource_kind[0]] = {}
        data["changes"]["deprecations"][resource_kind[0]] = {}
        data["changes"]["updates"][resource_kind[0]] = {}
        for child in root.findall(resource_kind[1]):
            if child.find("Inserts") is not None:
                for subchild in child.find("Inserts").findall(resource_kind[2]):
                    data["changes"]["inserts"][resource_kind[0]].update(
                        resource_kind[3](subchild))
            if child.find("Updates") is not None:
                for child in child.find("Updates").findall(resource_kind[2]):
                    data["changes"]["updates"][resource_kind[0]].update(
                        resource_kind[3](child))
    return data
