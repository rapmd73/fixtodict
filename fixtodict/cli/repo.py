import click
import jsonpatch
import json
import yaml
import os
from checksumdir import dirhash
from jsonschema import validate

from . import cli
from .utils.options import opt_patch
from .utils.xml import read_xml_root
from .utils.json import read_json, DEFAULT_INDENT
from ..basic_repository import (
    xml_files_to_repository,
    FILENAME_ABBREVIATIONS,
    FILENAME_CATEGORIES,
    FILENAME_COMPONENTS,
    FILENAME_DATATYPES,
    FILENAME_ENUMS,
    FILENAME_FIELDS,
    FILENAME_MESSAGES,
    FILENAME_MSG_CONTENTS,
    FILENAME_SECTIONS,
)
from ..fix_version import FixVersion
from ..resources import JSON_SCHEMA

# From <https://stackoverflow.com/questions/16782112>.
# I have no idea what this does.
yaml.add_representer(
    dict,
    lambda self, data: yaml.representer.SafeRepresenter.represent_dict(
        self, data.items()
    ),
)


def read_xml_files(src: str):
    path = os.path.join(src, "Messages.xml")
    if os.path.exists(path):
        return {
            r[0]: read_xml_root(src, r[0], opt=r[1])
            for r in [
                (FILENAME_ABBREVIATIONS, True),
                (FILENAME_CATEGORIES, True),
                (FILENAME_COMPONENTS, True),
                (FILENAME_DATATYPES, True),
                (FILENAME_ENUMS, False),
                (FILENAME_FIELDS, False),
                (FILENAME_MESSAGES, False),
                (FILENAME_MSG_CONTENTS, False),
                (FILENAME_SECTIONS, True),
            ]
        }
    return None


def derive_target_filename(v: FixVersion, target_dir, ext="json"):
    return os.path.join(
        target_dir,
        "{}-{}-{}{}.{}".format(
            v["fix"],
            v["major"],
            v["minor"],
            "-sp" + v["sp"] if v["sp"] != "0" else "",
            ext,
        ),
    )


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("dst", nargs=1, type=click.Path(exists=True))
@opt_patch("patches")
def repo(src, dst, patches):
    """
    Transform original FIX Repository data into JSON.

    The resulting data will feature:

    \b
    - High-quality Markdown documentation obtained from several sources, plus
      minor improvements, e.g.
      * links to ISO standards,
      * RFC 2119 terms capitalization,
      * links for internal navigation,
      * markup, bold text, etc.
    - Full breakdown into fields and components.
    - Information about included Extension Packs.
    - General cleanup and improved data consistency across all FIX protocol
      versions.

    <SRC> is a directory pointing to input FIX Repository data ("Basic"
    flavor only, "Intermediate" and "Unified" is not accepted). Specifically,
    FIXtodict will look for the following files inside <SRC>:

    \b
    - `Abbreviation.xml`
    - `Categories.xml`
    - `Components.xml`
    - `Datatypes.xml`
    - `Fields.xml`
    - `Sections.xml`
    - `Messages.xml`
    - `MsgContents.xml`

    Note: not all of these are mandatory. Future versions of FIXtodict might
    look for additional files.

    Output data is written to <DST>, which must be an existing directory.
    Filenames are properly generated according to FIX protocol version. Old
    files in <DST> might get overwritten WITHOUT BACKUP!
    """
    xml_files = read_xml_files(src)
    data = xml_files_to_repository(xml_files)
    data["fixtodict"]["md5"] = dirhash(src, "md5")
    validate(instance=data, schema=JSON_SCHEMA)
    for p in patches:
        patch = jsonpatch.JsonPatch(read_json(p))
        data = patch.apply(data)
    validate(instance=data, schema=JSON_SCHEMA)
    # Write output to file.
    filename = derive_target_filename(dst, data["version"])
    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=DEFAULT_INDENT))
        print("-- Written to '{}'".format(filename))
