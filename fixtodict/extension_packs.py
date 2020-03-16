from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from dict_recursive_update import recursive_update
import jsonpatch

from .basic_repository import *


def extension_pack_to_json_patch(ep):
    data = []
    changes = ep["changes"]
    for kind in ["abbreviations", "datatypes"]:
        for (key, value) in changes["added"][kind].items():
            data.append({
                "op": "add",
                "path": "/{}/{}".format(kind, key),
                "value": value
            })
        for (key, value) in changes["updated"][kind].items():
            for (child_key, child_value) in value.items():
                data.append({
                    "op": "replace",
                    "path": "/{}/{}/{}".format(kind, key, child_key),
                    "value": child_value
                })
        for (key, value) in changes["deprecated"]["abbreviations"].items():
            pass
            # original["abbreviations"] = recursive_update(original["abbreviations"],
        for key in changes["removed"][kind].keys():
            data.append({
                "op": "remove",
                "path": "/{}/{}".format(kind, key),
            })
    return jsonpatch.JsonPatch(data)


def apply_extension_pack(original, ep):
    changes = ep["changes"]
    for (key, value) in changes["added"]["abbreviations"].items():
        original["abbreviations"][key] = value
    for (key, value) in changes["updated"]["abbreviations"].items():
        original["abbreviations"] = recursive_update(original["abbreviations"],
                                                     {key: value})
    for (key, value) in changes["deprecated"]["abbreviations"].items():
        original["abbreviations"] = recursive_update(original["abbreviations"],
                                                     {key: value})
    for abbr in changes["removed"]["abbreviations"]:
        del original["abbreviations"][abbr[0]]
    return original


def extension_pack_from_path(path):
    xml = ElementTree.parse(path).getroot()[0]
    return xml_to_extension_pack(xml)


def xml_to_extension_pack(root: Element):
    root = root[0]
    data = {}
    data["id"] = root.get("id")
    data["approved"] = root.get("approved")
    data["description"] = root.get("desc")
    data["changes"] = {}
    data["changes"]["added"] = {}
    data["changes"]["updated"] = {}
    data["changes"]["deprecated"] = {}
    data["changes"]["removed"] = {}
    resource_kinds = [
        [
            "abbreviations", "Abbreviations", "Abbreviation",
            xml_to_abbreviation
        ],
        ["components", "Components", "Component", xml_to_component],  # FIXME
        ["datatypes", "Datatypes", "Datatype", xml_to_datatype],
        ["fields", "Fields", "Field", xml_to_field],
        ["categories", "Categories", "Category", xml_to_category],
        ["sections", "Sections", "Section", xml_to_section],
    ]
    for resource_kind in resource_kinds:
        data["changes"]["added"][resource_kind[0]] = {}
        data["changes"]["updated"][resource_kind[0]] = {}
        data["changes"]["deprecated"][resource_kind[0]] = {}
        data["changes"]["removed"][resource_kind[0]] = {}
        for child in root.findall(resource_kind[1]):
            added = child.find("Inserts")
            updated = child.find("Updates")
            if added is not None:
                for subchild in added.findall(resource_kind[2]):
                    data["changes"]["added"][resource_kind[0]].update(
                        dict([resource_kind[3](subchild)]))
            if updated is not None:
                for child in updated.findall(resource_kind[2]):
                    data["changes"]["updated"][resource_kind[0]].update(
                        dict([resource_kind[3](child)]))
    return data
