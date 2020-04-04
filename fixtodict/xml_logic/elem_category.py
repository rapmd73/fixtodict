from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    xml_get_component_type,
    filter_none,
)


def xml_to_categories(root):
    return xml_to_sorted_dict(root, xml_to_category)


def xml_to_category(root):
    return (
        # Primary key.
        root.findtext("CategoryID") or root.get("id"),
        {
            "kind": xml_get_component_type(root),
            "section": root.get("section") or root.findtext("SectionID"),
            "fixml": {
                "filename": root.get("FIXMLFileName")
                or root.findtext("FIXMLFileName"),
                "generateImpl": root.get("generateImplFile")
                or root.findtext("GenerateImplFile"),
                "optional": bool(
                    int(root.get("notReqXML") or root.findtext("NotReqXML"))
                ),
            },
            "docs": xml_get_docs(root, body=True, volume=True),
            "history": xml_get_history(root),
        },
    )
