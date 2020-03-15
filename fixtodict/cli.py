#!/usr/bin/env python3

import click
import jsonpatch
from checksumdir import dirhash
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from jsonschema import validate
import pkg_resources
import test
import sys
import json
import os

from api import xml_files_to_fix_dict
from extension_packs import xml_to_extension_pack, extension_pack_to_json_patch
from description import fix_dict_replace_typos
from utils import target_filename
from schema import SCHEMA
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


def read_json(path):
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except:
        err(path)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("dst", nargs=1, type=click.Path(exists=True))
@click.option(
    "--ep",
    "ep_files",
    multiple=True,
    help="Include this Expansion Pack file (.xml) into the final Fix Dictionary.",
    type=click.Path(exists=True),
)
@click.option(
    "--markdownify",
    "-m",
    default=False,
    help="Perform data enhancing on documentation strings. Off by default.",
    type=click.BOOL,
)
@click.option(
    "--typos",
    "typo_files",
    multiple=True,
    help="Provide a JSON typos file.",
    type=click.Path(exists=True),
)
@click.option(
    "--patch",
    "-p",
    "patches",
    multiple=True,
    help="Provide a JSON Patch file to apply to final data. Follows RFC 6902.",
    type=click.Path(exists=True),
)
@click.option(
    "--minify",
    "-m",
    default=False,
    help="Minify output JSON. Off by default.",
    type=click.BOOL,
)
@click.version_option(__version__)
def gen(src, dst, ep_files, markdownify, minify, typo_files, patches):
    """
    FIX Dictionary generator tool.

    \b
    # Copyright (c) 2020, Filippo Costa. Released under Apache License 2.0.
    # <https://www.apache.org/licenses/LICENSE-2.0.txt>
    # Find me on Github: <https://github.com/neysofu>

    This program performs data enhancing and data sanitazion on raw FIX
    Repository files. The dataing data will feature:

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
    data = xml_files_to_fix_dict(xml_files)
    data["fixtodict"]["md5"] = dirhash(src, "md5")
    if markdownify:
        data = markdownify_docs(data)
    # Fix typos in original documentation.
    for f in typo_files:
        data = fix_dict_replace_typos(data, read_json(f))
    validate(instance=data, schema=SCHEMA)
    for ep_f in ep_files:
        root = read_xml_ep(ep_f)
        ep = xml_to_extension_pack(root)
        patch = extension_pack_to_json_patch(ep)
        data = patch.apply(data)
    validate(instance=data, schema=SCHEMA)
    for p in patches:
        patch = jsonpatch.JsonPatch(read_json(p))
        data = patch.apply(data)
    validate(instance=data, schema=SCHEMA)
    # Write output to file.
    filename = target_filename(dst, data["version"])
    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=json_indent))
        print("-- Written to '{}'".format(filename))


@cli.command()
@click.argument("repo", nargs=1, type=click.Path(exists=True))
def review(repo):
    """
    Short review of FIXtodict output.
    """
    repo = read_json(repo)
    print("FIXtodict-flavoured FIX Repository data.")
    print("Abbreviations: {:>4}".format(len(repo["abbreviations"])))
    print("Datatypes:     {:>4}".format(len(repo["datatypes"])))
    print("Components:    {:>4}".format(len(repo["components"])))
    print("Fields:        {:>4}".format(len(repo["fields"])))
    print("Messages:      {:>4}".format(len(repo["messages"])))


@cli.command("diff-history")
@click.argument("old", nargs=1, type=click.Path(exists=True))
@click.argument("new", nargs=1, type=click.Path(exists=True))
@click.option(
    "--minify",
    "-m",
    default=False,
    help="Minify output JSON. Off by default.",
    type=click.BOOL,
)
def diff_history(old, new, minify):
    """
    Traces FIX Repository history by comparing old vs new data.
    """
    json_indent = None if minify else 2
    old_filename = old
    new_filename = new
    old = read_json(old)
    new = read_json(new)
    for kind in ["abbreviations", "datatypes", "fields", "components", "messages"]:
        for (key, value) in new[kind].items():
            def log(op): return print(
                "-- New [{}] diff for kind {}: {}".format(op, kind, key))
            if key not in old[kind]:
                log(" ADDED ")
                value["history"]["added"] = new["version"]
            elif old[kind][key] != value:
                log("UPDATED")
                value["history"]["updated"] = new["version"]
        for (key, value) in old[kind].items():
            def log(op): return print(
                "-- New [{}] diff for kind {}: {}".format(op, kind, key))
            if key not in new[kind]:
                log("REMOVED")
                old[kind][key]["history"]["removed"] = new["version"]
    with open(new_filename, "w") as f:
        f.write(json.dumps(new, indent=json_indent))
        print("-- Written to '{}'".format(new_filename))
    with open(old_filename, "w") as f:
        f.write(json.dumps(old, indent=json_indent))
        print("-- Written to '{}'".format(old_filename))


if __name__ == "__main__":
    cli()
