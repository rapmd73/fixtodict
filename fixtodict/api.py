import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from typing import List, Optional
from .utils import parse_protocol_version
from .repo_unified import (xml_to_abbreviations, xml_to_categories, xml_to_components,
                           xml_to_datatypes, xml_to_fields, xml_to_message_entities, xml_to_messages, xml_to_sections)


def onixs_dictionary_link(v_fields: List[str]):
    return "https://www.onixs.biz/fix-dictionary/{}{}.{}.SP{}/index.html".format(
        "" if v_fields[0] == "fix" else v_fields[0], *v_fields[1:])


def fixopaedia_dictionary_link(v_fields: List[str]):
    return "https://btobits.com/fixopaedia/fixdict{}{}{}/index.html".format(
        v_fields[1], v_fields[2],
        "" if int(v_fields[3]) == 0 else "-sp{}".format(v_fields[3]))


def fixipe_dictionary_link(v_fields: List[str]):
    return "https://fixipe.com/#/explore/{}/{}.{}/servicepack/{}".format(
        *v_fields)


def generate_links(v_fields: List[str]):
    return {
        "onixsDictionary": onixs_dictionary_link(v_fields),
        "fixipeDictionary": fixipe_dictionary_link(v_fields),
        "fixoapediaDictionary": fixopaedia_dictionary_link(v_fields),
    }


def xml_to_fix_dictionary(root: Element):
    version = root.get("version")
    return {
        "version": version,
        "fixml": root.get("fixml") == "1",
        # Let's ignore the "specUrl" attributes becauses it gives 404.
        "links": generate_links(parse_protocol_version(version)),
        # "ep": beautify_extension_packs(root.find("manifest")),
        "abbreviations": xml_to_abbreviations(root.find("abbreviations")),
        "datatypes": xml_to_datatypes(root.find("datatypes")),
        "sections": xml_to_sections(root.find("sections")),
        "categories": xml_to_categories(root.find("categories")),
        "fields": xml_to_fields(root.find("fields")),
        "components": xml_to_components(root.find("components")),
        "messages": xml_to_messages(root.find("messages")),
    }
