from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    filter_none,
    get_fuzzy,
)


def xml_to_messages(root):
    return xml_to_sorted_dict(root, xml_to_message)


def xml_to_message(root):
    return (
        # Primary key.
        get_fuzzy(root, "msgType"),
        {
            "$component": get_fuzzy(root, "id", "ComponentID"),
            "name": get_fuzzy(root, "Name"),
            "contents": xml_to_refs(root),
            "category": get_fuzzy(root, "Category", "CategoryID"),
            "section": get_fuzzy(root, "Section", "SectionID"),
            "fixml": {
                "optional": (lambda x: bool(int(x)) if x is not None else None)(
                    get_fuzzy(root, "NotReqXML")
                ),
            },
            "docs": xml_get_docs(root, body=True, elaboration=True),
            "history": xml_get_history(root),
        },
    )


def xml_to_refs(root):
    component_id = get_fuzzy(root, "id", "ComponentID")
    data = {}
    for child in root:
        pass


def embed_msg_contents_into_message(message, msg_contents):
    message["contents"] = msg_contents[message["$component"]]
    del message["$component"]
