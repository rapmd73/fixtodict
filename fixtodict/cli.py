#!/usr/bin/env python3

import click
from checksumdir import dirhash
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import test
import sys
import json
import os

from api import xml_files_to_fix_dict
from docs import xml_to_docs, markdownify_docs, needs_docs, embed_docs_into_data
from extension_packs import xml_to_extension_pack, apply_extension_pack
from utils import target_filename
from version import __version__


def err(path):
    print("Error: Invalid XML file.")
    exit(-1)


def read_xml_files(src: str):
    path = os.path.join(src, "Messages.xml")
    if os.path.exists(path):
        return {
            "abbreviations": read_xml_root(src, "Abbreviations.xml"),
            "categories": read_xml_root(src, "Categories.xml"),
            "components": read_xml_root(src, "Components.xml"),
            "datatypes": read_xml_root(src, "Datatypes.xml"),
            "enums": read_xml_root(src, "Enums.xml", opt=False),
            "fields": read_xml_root(src, "Fields.xml", opt=False),
            "messages": read_xml_root(src, "Messages.xml", opt=False),
            "msg_contents": read_xml_root(src, "MsgContents.xml", opt=False),
            "sections": read_xml_root(src, "Sections.xml"),
        }
    return None


def read_xml_root(src, filename, opt=True):
    path = os.path.join(src, filename)
    try:
        return ElementTree.parse(path).getroot()
    except:
        if not opt:
            err(path)
    return None


def read_xml_ep(path):
    try:
        return ElementTree.parse(path).getroot()
    except:
        err(path)


@click.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("dst", nargs=1, type=click.Path(exists=True))
@click.option(
    "--ep", "ep_files",
    multiple=True,
    help="Include this Expansion Pack file (.xml) into the final Fix Dictionary.",
    type=click.Path(exists=True),
)
@click.option(
    "--markdownify", "-m",
    default=False,
    help="Perform data enhancing on documentation strings. Off by default.",
    type=click.BOOL,
)
@click.option(
    "--minify", "-m",
    default=False,
    help="Minify output JSON. Off by default.",
    type=click.BOOL,
)
@click.version_option(__version__)
def main(src, dst, ep_files, markdownify, minify):
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
      * RFC 2119 terms capitalization,
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
    this program will look for the following files inside <SRC>:

    \b
    - `Abbreviation.xml`
    - `Components.xml`
    - `Datatypes.xml`
    - `Fields.xml`
    - `MsgContents.xml`
    - `MsgType.xml`

    Future versions of this program might look for additional files.

    Output data is written to <DST>, which must be an existing directory.
    Filenames are properly generated according to FIX protocol version. Old
    files in <DST> might get overwritten WITHOUT BACKUP!
    """
    json_indent = None if minify else 2
    xml_files = read_xml_files(src)
    result = xml_files_to_fix_dict(xml_files)
    ep = []
    for filename in ep_files:
        root = read_xml_ep(filename)
        ep.append(xml_to_extension_pack(root))
    if markdownify:
        result = markdownify_docs(result)
    result["fixtodict"]["md5"] = dirhash(src, "md5")
    # Apply EPs.
    for x in ep:
        result = apply_extension_pack(result, x)
    # Write output to file.
    filename = target_filename(dst, result["version"])
    with open(filename, "w") as f:
        f.write(json.dumps(result, indent=json_indent))
        print("-- Written to '{}'".format(filename))


if __name__ == "__main__":
    main()
