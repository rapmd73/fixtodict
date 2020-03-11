#!/usr/bin/env python3

import sys
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import click
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from typing import List, Optional
import unittest
import json

# BASIC REPOSITORY JSON CONVERTER
# -------------------------------


def basic_abbreviations(root: Element):
    if root is None:
        return {}
    data = {}
    for child in sorted(root, key=lambda c: c.get("abbrTerm")):
        data.update(dict(basic_abbreviation(child)))
    return data


def basic_abbreviation(root: Element):
    name = root.find("AbbrTerm").text
    data = {}
    if root.get("Term") is not None:
        data["term"] = root.get("Term")
    if root.find("Term") is not None:
        data["term"] = root.find("Term").text
    if root.find("Usage") is not None:
        data["usage"] = root.find("Usage").text
    if root.get("added") is not None:
        data["added"] = protocol_from_xml_attrs(root.attrib)
    return {name: data}


def basic_datatype(root: Element):
    name = root.find("Name").text
    data = {}
    if root.find("BaseType") is not None:
        data["baseDatatype"] = root.find("BaseType").text
    if root.find("Description") is not None:
        data["description"] = root.find("Description").text
    if root.find("Example") is not None:
        data["examples"] = []
        for e in root.findall("Example"):
            data["examples"].append(e.text)
    if root.get("added") is not None:
        data["added"] = protocol_from_xml_attrs(root.attrib)
    return {name: data}


def basic_field(root: Element):
    data = {}
    if root.find("Name") is not None:
        data["name"] = root.find("Name").text
    if root.find("Type") is not None:
        data["type"] = root.find("Type").text
    if root.find("Description") is not None:
        data["description"] = root.find("Description").text
    if root.find("Elaboration") is not None:
        data["elaboration"] = root.find("Elaboration").text
    return {root.get("Tag"): data}


def basic_component(root: Element):
    data = {}
    if root.find("Name") is not None:
        data["name"] = root.find("Name").text
    if root.get("ComponentID") is not None:
        data["id"] = root.get("ComponentID").text
    if root.find("ComponentType") is not None:
        data["kind"] = root.find("ComponentType").text
    if root.find("CategoryID") is not None:
        data["category"] = root.find("CategoryId").text
    if root.find("Description") is not None:
        data["description"] = root.find("Description").text
    return {root.get("Tag"): data}


# HELPER FUNCTIONS
# ----------------


def iso_link(iso: str):
    return '[ISO {0}](https://en.wikipedia.org/wiki/ISO_{0})'.format(iso)


def datatype_link(dt: str):
    return '[`{0}`](#/datatypes/{0})'.format(dt)


def onixs_dictionary_link(version: List[str]):
    return "https://www.onixs.biz/fix-dictionary/{}{}.{}.SP{}/index.html".format(
        "" if version[0] == "fix" else version[0], *version[1:])


def fixopaedia_dictionary_link(version: List[str]):
    return "https://btobits.com/fixopaedia/fixdict{}{}{}/index.html".format(
        version[1], version[2],
        "" if int(version[3]) == 0 else "-sp{}".format(version[3]))


def fixipe_dictionary_link(version: List[str]):
    return "https://fixipe.com/#/explore/{}/{}.{}/servicepack/{}".format(
        *version)


def generate_links(version: List[str]):
    return {
        "onixsDictionary": onixs_dictionary_link(version),
        "fixipeDictionary": fixipe_dictionary_link(version),
        "fixoapediaDictionary": fixopaedia_dictionary_link(version),
    }


def parse_protocol_version(val: str, ep: str = "-1"):
    """
    Parses a string that represents a FIX protocol version into its original
    fields.
    """
    # Explicit servicepack tagging.
    if "SP" in val:
        protocol, servicepack = tuple(val.split("SP"))
    else:
        protocol, servicepack = val, "0"
    protocol, major, minor = tuple(protocol.split("."))
    protocol = protocol.lower()
    if ep == "-1":
        return [protocol, major, minor, servicepack]
    else:
        return [protocol, major, minor, servicepack, ep]


def protocol_from_xml_attrs(d: dict):
    if "addedEP" in d:
        return parse_protocol_version(d["added"], d["addedEP"])
    else:
        return parse_protocol_version(d["added"])


def read_docs(parent_dir: str, version: str):
    path = os.path.join(parent_dir, "{}_en_phrases.xml".format(version))
    try:
        return ElementTree.parse(path).getroot()
    except IOError:
        print("Error: Couldn't locale file '{}'.")
        exit(-1)


def target_filename(target_dir, version: List[str]):
    return os.path.join(
        target_dir, "{}-{}-{}{}.json".format(
            version[0], version[1], version[2],
            "-sp" + version[3] if version[3] != "0" else ""))


def breakdown_contents(root: Element):
    data = []
    i = 0
    for child in root:
        data.append({})
        data[i]["id"] = child.get("id")
        data[i]["name"] = child.get("name")
        data[i]["kind"] = "field" if child.tag == "fieldRef" else "component"
        data[i]["required"] = child.get("required") == "1"
        data[i]["description"] = child.get("text")
        i += 1
    return data


# DATA BEAUTIFIERS
# ----------------


def beautify_extension_packs(root: Element):
    if root is None:
        return {}
    data = {}
    for child in sorted(root, key=lambda c: int(c.get("id"))):
        key = int(child.get("id"))
        data[key] = {}
        data[key]["description"] = child.text
    return data


def beautify_datatypes(root: Element):
    data = {}
    for child in root:
        name = child.get("name")
        data[name] = {}
        base_datatype = child.get("baseType")
        if base_datatype:
            data[name]["baseDatatype"] = base_datatype
        data[name]["description"] = child.get("text")
        xml_details = child.find("XML")
        if xml_details is not None:
            data[name]["xmlBaseDatatype"] = xml_details.get("base")
            data[name]["xmlBuiltIn"] = xml_details.get("builtin") == "1"
            data[name]["xmlDescription"] = child.get("text")
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def beautify_sections(root: Optional[Element]):
    if root is None:
        return {}
    data = {}
    for child in sorted(root, key=lambda c: c.get("id")):
        name = child.get("id")
        data[name] = {}
        data[name]["description"] = child.get("text")
    return data


def beautify_categories(root: Optional[Element]):
    if root is None:
        return {}
    data = {}
    for child in sorted(root, key=lambda c: c.get("id")):
        name = child.get("id")
        data[name] = {}
        data[name]["section"] = child.get("section")
        data[name]["volume"] = child.get("volume")
    return data


def beautify_abbreviations(root: Optional[Element]):
    if root is None:
        return {}
    data = {}
    for child in sorted(root, key=lambda c: c.get("abbrTerm")):
        name = child.get("abbrTerm")
        data[name] = {}
        # "usage" attribute doesn't seem used at all, so let's ignore it.
        data[name]["term"] = child.get("text")
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def beautify_fields(root: Element):
    data = {}
    for child in sorted(root, key=lambda c: int(c.get("id"))):
        name = child.get("name")
        data[name] = {}
        data[name]["id"] = child.get("id")
        data[name]["description"] = child.get("text")
        data[name]["datatype"] = child.get("type")
        data[name]["enums"] = child.get("type")
        if len(child) > 0:
            data[name]["enums"] = {}
        for subchild in child:
            val = subchild.get("value")
            data[name]["enums"][val] = {}
            e = data[name]["enums"][val]
            e["name"] = subchild.get("symbolicName")
            e["description"] = subchild.get("text")
            e["added"] = protocol_from_xml_attrs({
                **child.attrib,
                **subchild.attrib
            })
        try:
            data[name]["requiredFixml"] = child.get("notReqXML") == "0"
        except:
            pass
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def beautify_components(root: Element):
    data = {}
    for child in sorted(root, key=lambda c: int(c.get("id"))):
        name = child.get("name")
        data[name] = {}
        data[name]["id"] = child.get("id")
        data[name]["name"] = child.get("name")
        data[name]["category"] = child.get("category")
        data[name]["kind"] = child.get("type")
        data[name]["isRepeating"] = child.get("repeating") == "1"
        data[name]["description"] = child.get("text")
        data[name]["contents"] = breakdown_contents(child)
        try:
            data[name]["requiredFixml"] = item["@notReqXML"] == "0"
        except:
            pass
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def beautify_messages(root: Element):
    data = {}
    for child in sorted(root, key=lambda c: int(c.get("id"))):
        name = child.get("name")
        data = {}
        data[name] = {}
        data[name]["id"] = child.get("id")
        data[name]["category"] = child.get("category")
        data[name]["section"] = child.get("section")
        data[name]["contents"] = breakdown_contents(child)
        data[name]["requiredFixml"] = child.get("notReqXML") == "0"
        data[name]["added"] = protocol_from_xml_attrs(child.attrib)
    return data


def beautify_data(root: Element, docs):
    root = embed_docs(root, docs)
    version = root.get("version")
    return {
        "version": version,
        "fixml": root.get("fixml") == "1",
        "copyright": "",
        "generatedAt": root.get("generated"),
        # Let's ignore the "specUrl" attributes becauses it gives 404.
        "links": generate_links(parse_protocol_version(version)),
        "ep": beautify_extension_packs(root.find("manifest")),
        "datatypes": beautify_datatypes(root.find("datatypes")),
        "sections": beautify_sections(root.find("sections")),
        "categories": beautify_categories(root.find("categories")),
        "fields": beautify_fields(root.find("fields")),
        "components": beautify_components(root.find("components")),
        "messages": beautify_messages(root.find("messages")),
        "abbreviations": beautify_abbreviations(root.find("abbreviations")),
    }


# TEXT PROCESSING
# ---------------


def improve_description(content: str, kind: str):
    # Detect abbreviations. They have very short descriptions and don't require
    # additional preprocessing.
    if kind == "AT":
        return content
    words = nltk.word_tokenize(content, preserve_line=True)
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


def preprocess_docs(docs: Element, improve_descr: bool):
    # Right now it's a big array, but we need direct access by key.
    data = {item.get("textId"): item for item in docs}
    for (key, val) in data.items():
        # Empty description.
        if len(val) == 0:
            data[key] = None
        elif improve_descr:
            kind = key.split("_")[0]
            data[key] = "\n".join(
                [improve_description(p.text, kind) for p in val[0]])
        # Leave it as it is and just merge paragraphs.
        else:
            data[key] = "\n".join([p.text for p in val[0]])
    return data


# MAIN LOGIC
# -----------


def embed_docs(root_element: Element, docs):
    for child in root_element:
        if "textId" in child.keys():
            child.set("text", docs[child.get("textId")])
        embed_docs(child, docs)
    return root_element


def read_repositories(src: str):
    path = os.path.join(src, "FixRepository.xml")
    if not os.path.isfile(path):
        path = os.path.join(src, "IntermediateRepository.xml")
    if not os.path.isfile(path):
        print("Error: Can't locate a valid FIX Repository file.")
        exit(-1)
    try:
        return ElementTree.parse(path).getroot()
    except:
        print("Error: Invalid XML file.")
        exit(-1)


@click.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("dst", nargs=1, type=click.Path(exists=True))
@click.option(
    "--ep",
    multiple=True,
    help=
    "Include this Expansion Pack file (.xml) into the final Fix Dictionary.",
    type=click.Path(exists=True),
)
@click.option(
    "--docs",
    "docs_path",
    default="",
    help=
    "Alternative source directory for documentation files. Same as <SRC> by default.",
    type=click.Path())
@click.option(
    "--improve-docs",
    default=False,
    help="Perform data enhancing on documentation strings. Off by default.",
    type=click.BOOL,
)
def main(src, dst, improve_docs, ep, docs_path):
    """
    FIX Dictionary generator tool.
    
    \b
    # Copyright (c) 2020, Filippo Costa. Released under Apache License 2.0.
    # <https://www.apache.org/licenses/LICENSE-2.0.txt>
    # Find me on Github: <https://github.com/neysofu>

    This program performs data enhancing and data sanitazion on raw FIX
    Repository files. The resulting data will feature:

    \b
    - High-quality Markdown documentation obtained from several sources, plus
      minor improvements, e.g.
      * links to ISO standards,
      * RFC 2119 terms highlight,
      * links for internal navigation,
      * markup, bold text, etc.
    - Embedded documentation strings (instead of separate files, like the
      original FIX Repository).
    - Full breakdown into fields and components.
    - Information about included Extension Packs.
    - General cleanup and improved data consistency across all FIX protocol
      versions.

    Moreover, all output data is valid JSON for easier consumption.

    <SRC> is a directory pointing to input FIX Repository data. Specifically,
    inside <SRC> the program will look for any of these two files (in this
    order; they are treated equally):

    \b
    - `FixRepository.xml` (unified FIX Repository).
    - `IntermediateRepository.xml` (intermediate FIX Repository).

    <SRC> should also contain appropriate documentation files (e.g.
    `FIX.4.4_en_phrases.xml`). Future versions of this program might look for
    additional files.

    Output data is written to <DST>, which must be an existing directory.
    Filenames are properly generated according to FIX protocol version. Old
    files in <DST> might get overwritten WITHOUT BACKUP!
    """
    repositories = read_repositories(src)
    # We now have definitions for several versions of the protocol. Each must
    # be processed separately.
    for repo_xml in repositories:
        version = repo_xml.get("version")
        docs_xml = read_docs(docs_path or src, version)
        docs = preprocess_docs(docs_xml, improve_docs)
        result = beautify_data(repo_xml, docs)
        version = parse_protocol_version(version)
        filename = target_filename(dst, version)
        with open(filename, "w") as f:
            f.write(json.dumps(result, indent=2))
            print("Written to '{}'.".format(filename))


# TESTS
# -----


class TestBasicRepository(unittest.TestCase):

    ABBREVIATIONS_XML = [
        """
        <Abbreviation Term="Funding">
            <AbbrTerm>Fndng</AbbrTerm>
            <Usage>FundingSource component</Usage>
        </Abbreviation>
        """, """
        <Abbreviation added="FIX.5.0SP1" addedEP="77">
            <Term>Detail</Term>
            <AbbrTerm>Detl</AbbrTerm>
        </Abbreviation>
        """, """
        <Abbreviation added="FIX.4.4">
           <Term>ExchangeForPhysical</Term>
           <AbbrTerm>EFP</AbbrTerm>
        </Abbreviation>
        """
    ]

    ABBREVIATIONS_DICT = [{
        "Fndng": {
            "term": "Funding",
            "usage": "FundingSource component",
        }
    }, {
        "Detl": {
            "term": "Detail",
            "added": ["fix", "5", "0", "1", "77"]
        }
    }, {
        "EFP": {
            "term": "ExchangeForPhysical",
            "added": ["fix", "4", "4", "0"]
        }
    }]

    def test_abbreviation(self):
        for (s, expected) in zip(TestBasicRepository.ABBREVIATIONS_XML,
                                 TestBasicRepository.ABBREVIATIONS_DICT):
            xml = ElementTree.fromstring(s)
            actual = basic_abbreviation(xml)
            self.assertEqual(actual, expected)

    DATATYPES_XML = [
        """
        <Datatype added="FIX.4.3">
            <Name>Length</Name>
            <BaseType>int</BaseType>
            <Description>lulz</Description>
            <XML>
                <BuiltIn>0</BuiltIn>
                <Base>xs:nonNegativeInteger</Base>
            </XML>
        </Datatype>
        """, """
        <Datatype added="FIX.4.2">
            <Name>LocalMktDate</Name>
            <BaseType>String</BaseType>
            <Description>foobar</Description>
            <Example>BizDate="2003-09-10"</Example>
            <XML>
                <BuiltIn>0</BuiltIn>
                <Base>xs:date</Base>
                <Description>spam</Description>
                <Example>BizDate="2003-09-10"</Example>
            </XML>
        </Datatype>
        """
    ]

    DATATYPES_DICT = [{
        "Length": {
            "baseDatatype": "int",
            "description": "lulz",
            "added": ['fix', '4', '3', '0'],
        }
    }, {
        "LocalMktDate": {
            "baseDatatype": "String",
            "examples": ['BizDate="2003-09-10"'],
            "description": "foobar",
            "added": ['fix', '4', '2', '0'],
        }
    }]

    def test_datatypes(self):
        for (s, expected) in zip(TestBasicRepository.DATATYPES_XML,
                                 TestBasicRepository.DATATYPES_DICT):
            xml = ElementTree.fromstring(s)
            actual = basic_datatype(xml)
            self.assertEqual(actual, expected)

    FIELDS_XML = [
        """
        <Field Tag="2841">
            <Name>UnderlyingRefID</Name>
            <Type>String</Type>
            <AbbrName>UndlyRefID</AbbrName>
            <NotReqXML>0</NotReqXML>
            <Description>Identifies ...</Description>
        </Field>
        """
    ]

    FIELDS_DICT = [{
        "2841": {
            "name": "UnderlyingRefID",
            "type": "String",
            "description": "Identifies ..."
        }
    }]

    def test_fields(self):
        for (s, expected) in zip(TestBasicRepository.FIELDS_XML,
                                 TestBasicRepository.FIELDS_DICT):
            xml = ElementTree.fromstring(s)
            actual = basic_field(xml)
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    if sys.argv[1] == "test":
        unittest.main(argv=["fixdict"])
    else:
        main()
