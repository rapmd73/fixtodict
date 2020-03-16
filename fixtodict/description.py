import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from xml.etree.ElementTree import Element


def iso_link(iso: str):
    return '[ISO {0}](https://en.wikipedia.org/wiki/ISO_{0})'.format(iso)


def datatype_link(dt: str):
    return '[`{0}`](#/datatypes/{0})'.format(dt)


def beautify_docs(data, kind: str):
    # Detect abbreviations. They have very short descriptions and don't require
    # additional preprocessing.
    if kind == "AT":
        return data
    words = nltk.word_tokenize(data, preserve_line=True)
    # Link references to primitive datatypes.
    if len(words) >= 2 and words[1] == "field":
        words[0] = datatype_link(words[0])
    # Put examples in their own section.
    elif 1 >= len(words) >= 3 and words[0].lower().startswith("example"):
        words[0] = "# Examples"
    i = 0
    while i < len(words):
        # Capitalize RFC 2119 terms.
        if words[i] in ["might", "may", "must", "should"]:
            words[i] = words[i].upper()
            if words[i + 1] in ["not", "to"]:
                words[i + 1] = words[i + 1].upper()
        # Embed links to Wikipedia pages for ISO standards.
        if words[i] == "ISO":
            # Replace the next word with a link and remove this one.
            words[i + 1] = iso_link(words[i + 1])
            del words[i]
        else:
            i += 1
        i += 1
    return TreebankWordDetokenizer().detokenize(words)


def xml_to_docs(root: Element):
    # Right now it's a big array, but we need direct access by key.
    data = {item.get("textId"): item for item in root}
    for (key, val) in data.items():
        # Empty description.
        if len(val) == 0:
            data[key] = None
        else:
            data[key] = {"paragraphs": [p.text for p in val[0]]}
    return data


def markdownify_docs(docs):
    for (key, val) in docs.items():
        kind = key.split("_")[0]
        docs[key] = "\n".join(
            [beautify_docs(p, kind) for p in val["paragraphs"]])
    return docs


def embed_docs_into_data(data, docs):
    if isinstance(data, dict):
        for (key, val) in data.items():
            if key == "description":
                data[key] = docs[val]
            else:
                data[key] = embed_docs_into_data(val, docs)
    elif isinstance(data, list):
        data = [embed_docs_into_data(x, docs) for x in data]
    return data


def transform_descriptions(data, f):
    if isinstance(data, dict):
        for (key, val) in data.items():
            if key == "description":
                data[key] = f(val)
            else:
                data[key] = transform_descriptions(val, f)
    elif isinstance(data, list):
        data = [transform_descriptions(x, f) for x in data]
    return data


def fix_dict_replace_typos(data, typos):
    def replace(description):
        for kind in ["body", "usage", "volume", "elaboration"]:
            if kind in description and description[kind] is not None:
                for (old, new) in typos.items():
                    description[kind] = description[kind].replace(old, new)
        return description

    return transform_descriptions(data, replace)