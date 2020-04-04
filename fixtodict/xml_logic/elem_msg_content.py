from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    filter_none,
)


def xml_to_msg_contents(root):
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


def xml_to_msg_content(root):
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
