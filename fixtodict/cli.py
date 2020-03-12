import click
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import test
import sys
import json
import os
from .version import __version__
from .api import xml_to_fix_dictionary, parse_protocol_version
from .docs import xml_to_docs, beautify_docs
from .utils import iso8601_local, target_filename

LEGAL_INFO = 'FIXtodict is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'


def read_docs(parent_dir: str, version: str):
    path = os.path.join(parent_dir, "{}_en_phrases.xml".format(version))
    try:
        return ElementTree.parse(path).getroot()
    except IOError:
        print("Error: Couldn't locate file '{}'.")
        exit(-1)


def read_src(src: str):
    path = os.path.join(src, "FixRepository.xml")
    if not os.path.isfile(path):
        path = os.path.join(src, "IntermediateRepository.xml")
    if path is None:
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
    help="Include this Expansion Pack file (.xml) into the final Fix Dictionary.",
    type=click.Path(exists=True),
)
@click.option(
    "--docs",
    "docs_path",
    default="",
    help="Alternative source directory for documentation files. Same as <SRC> by default.",
    type=click.Path())
@click.option(
    "--improve-docs", "-i",
    default=False,
    help="Perform data enhancing on documentation strings. Off by default.",
    type=click.BOOL,
)
@click.option(
    "--minify", "-m",
    default=False,
    help="Minify output JSON. Off by default",
    type=click.BOOL,
)
@click.version_option(__version__)
def main(src, dst, improve_docs, ep, docs_path, minify):
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
    json_indent = None if minify else 2
    main_xml = read_src(src)
    # We now have definitions for several versions of the protocol. Each must
    # be processed separately.
    for repo_xml in main_xml:
        version = repo_xml.get("version")
        docs_xml = read_docs(docs_path or src, version)
        docs = xml_to_docs(docs_xml)
        result = {"FIXtodict": {
            "version": __version__,
            "legal": LEGAL_INFO,
            "command": " ".join(sys.argv),
            "generated": iso8601_local()
        }}
        result.update(xml_to_fix_dictionary(repo_xml, docs))
        filename = target_filename(dst, version)
        with open(filename, "w") as f:
            f.write(json.dumps(result, indent=json_indent))
            print("-- Written to '{}'".format(filename))
