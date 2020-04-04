from .utils import xml_to_sorted_dict, xml_get_docs, xml_get_history


def xml_to_abbreviations(root):
    return xml_to_sorted_dict(root, xml_to_abbreviation)


def xml_to_abbreviation(root):
    return (
        # Primary key.
        root.get("abbrTerm") or root.findtext("AbbrTerm"),
        {
            "term": root.get("term") or root.findtext("Term"),
            "docs": xml_get_docs(root, usage=True),
            "history": xml_get_history(root),
        },
    )
