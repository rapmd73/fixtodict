from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    filter_none,
)


def xml_to_messages(root):
    return xml_to_sorted_dict(root, xml_to_message)


def xml_to_message(root):
    return (
        # Primary key.
        root.get("msgType") or root.findtext("MsgType"),
        {
            "name": root.get("name") or root.findtext("Name"),
            "component": root.get("id") or root.findtext("ComponentID"),
            "category": root.get("category") or root.findtext("CategoryID"),
            "section": root.get("section") or root.findtext("SectionID"),
            "fixml": {
                "optional": bool(
                    int(root.get("notReqXML") or root.findtext("NotReqXML"))
                )
            },
            "docs": xml_get_docs(root, body=True, elaboration=True),
            "history": xml_get_history(root),
        },
    )


def embed_msg_contents_into_message(message, msg_contents):
    message["contents"] = msg_contents[message["component"]]
    del message["component"]
