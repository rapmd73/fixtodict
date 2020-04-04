from .utils import xml_to_sorted_dict, xml_get_docs, xml_get_history


def xml_to_phrases(root):
    return xml_to_sorted_dict(root, xml_to_phrase)


def xml_to_phrase(root):
    text = root.find("text")
    return (
        root.get("textId"),
        {
            "description": "\n".join([child.text for child in text.findall("para")]) + "\n",
            "abbreviationTerm": text.findtext("para"),
        },
    )


def embed_docs(data, phrases):
    for val in data.values():
        if isinstance(val["docs"], str):
            if val["docs"].startswith("AT_"):
                val["term"] = phrases[val["docs"]]["abbreviationTerm"]
            del phrases[val["docs"]]["abbreviationTerm"]
            val["docs"] = phrases[val["docs"]]
