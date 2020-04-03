import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from . import err


def strip_namespace(el: Element):
    if el.tag.startswith("{"):
        el.tag = el.tag.split('}', 1)[1]  # strip namespace
    for k in el.attrib.keys():
        if k.startswith("{"):
            k2 = k.split('}', 1)[1]
            el.attrib[k2] = el.attrib[k]
            del el.attrib[k]
    for child in el:
        strip_namespace(child)


def read_xml_root(src, filename, opt=True):
    path = os.path.join(src, filename)
    try:
        root = ElementTree.parse(path).getroot()
        strip_namespace(root)
        return root
    except (ElementTree.ParseError, FileNotFoundError):
        if not opt:
            err("XML")
    return None
