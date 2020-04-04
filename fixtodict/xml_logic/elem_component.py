from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    filter_none,
)


def xml_to_components(root):
    return xml_to_sorted_dict(root, xml_to_component)


def xml_to_component(root):
    kind = root.get("type") or root.findtext("ComponentType")
    return (
        # Primary key.
        root.get("id") or root.findtext("ComponentID"),
        {
            "name": root.get("name") or root.findtext("Name"),
            "nameAbbr": root.get("abbrName") or root.findtext("NameAbbr"),
            "kind": kind.lower() if kind else None,
            "category": root.get("category") or root.findtext("CategoryID"),
            "docs": xml_get_docs(root, body=True, elaboration=True),
            "history": xml_get_history(root),
        },
    )


def embed_msg_contents_into_component(component, id, msg_contents):
    component["contents"] = msg_contents[id]
