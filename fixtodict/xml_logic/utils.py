from ..fix_version import FixVersion


def filter_none(data):
    return {k: v for k, v in data.items() if v is not None}


def xml_get_history(root, replaced=False):
    data = {}
    keywords = ["added", "updated", "deprecated"]
    if replaced:
        keywords.append("replaced")
        if root.get("ReplacedByField") is not None:
            data["replacement"] = root.get("ReplacedByField")
    for keyword in keywords:
        version = FixVersion.create_from_xml_attrs(root.attrib, keyword)
        if version is not None:
            data[keyword] = version.data
    if root.get("issue"):
        data["issues"] = [root.get("issue")]
    return filter_none(data)


def xml_get_docs(
    root,
    body=False,
    usage=False,
    volume=False,
    elaboration=False,
    examples=False,
):
    data = {}
    if root.get("textId") is not None:
        return root.get("textId")
    if body:
        data["description"] = root.findtext("Description")
    if usage:
        data["usage"] = root.findtext("Usage")
    if volume:
        data["volume"] = root.findtext("Volume")
    if elaboration:
        data["elaboration"] = root.findtext("Elaboration")
    if examples:
        data["examples"] = [c.text for c in root.findall("Example")]
    return filter_none(data)


def xml_get_component_type(root):
    return str.lower(
        root.get("componentType") or root.findtext("ComponentType")
    )


def xml_to_sorted_dict(root, f):
    if root is None:
        root = []
    data = sorted([f(c) for c in root], key=lambda x: str.lower(x[0]))
    return {k: v for (k, v) in data}
