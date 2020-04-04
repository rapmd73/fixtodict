from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    filter_none,
)


def xml_to_sections(root):
    if root is None:
        root = []
    data = [xml_to_section(c) for c in root]
    return {k: v for (k, v) in data}


def xml_to_section(root):
    return (
        # Primary key.
        root.get("id") or root.findtext("SectionID"),
        {
            "name": root.get("name") or root.findtext("Name"),
            "fixml": {
                "filename": root.get("FIXMLFileName")
                or root.findtext("FIXMLFileName"),
                "optional": bool(
                    int(root.get("notReqXML") or root.findtext("NotReqXML"))
                ),
            },
            "docs": xml_get_docs(root, volume=True, body=True),
            "history": xml_get_history(root),
        },
    )
