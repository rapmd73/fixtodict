import os
from xml.etree import ElementTree

from . import err


def read_xml_root(src, filename, opt=True):
    path = os.path.join(src, filename)
    try:
        return ElementTree.parse(path).getroot()
    except ElementTree.ParseError:
        if not opt:
            err("XML")
    return None


def read_xml_ep(path):
    try:
        return ElementTree.parse(path).getroot()[0]
    except ElementTree.ParseError:
        err("XML")
