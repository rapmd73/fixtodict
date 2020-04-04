from .elem_enum import xml_to_enum
from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    filter_none,
)


def xml_to_fields(root):
    return xml_to_sorted_dict(root, xml_to_field)


def xml_to_field(root):
    return (
        # Primary key.
        root.findtext("Tag") or root.get("id"),
        filter_none(
            {
                "name": root.findtext("Name") or root.get("name"),
                "datatype": root.findtext("Type") or root.get("type"),
                "enum": xml_get_enum(root),
                "docs": xml_get_docs(root, body=True, elaboration=True),
                "history": xml_get_history(root),
            }
        ),
    )


def xml_get_enum(root):
    if len(root.findall("enum")) == 0:
        return root.findtext("EnumDatatype")
    return [xml_get_enum(child) for child in root]


def embed_enums_into_field(field, enums):
    if "enum" in field:
        field["enum"] = enums[field["enum"]]
