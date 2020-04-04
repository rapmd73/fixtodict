from .utils import xml_to_sorted_dict, xml_get_docs, xml_get_history


def xml_to_enums(root):
    data = {}
    for child in root:
        enum = xml_to_enum(child)
        parent = enum["parent"]
        if parent not in data:
            data[parent] = []
        del enum["parent"]
        data[parent].append(enum)
    return data


def xml_to_enum(root):
    return {
        "parent": root.findtext("Tag"),
        "name": root.findtext("SymbolicName"),
        "value": root.findtext("Value"),
        "history": xml_get_history(root),
        "docs": xml_get_docs(root),
    }
