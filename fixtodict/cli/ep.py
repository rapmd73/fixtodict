import click
import json

from . import cli
from ..extension_packs import xml_to_extension_pack, extension_pack_to_json_patch
from ..utils import read_xml_ep, JSON_INDENT


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("dst", nargs=1, type=click.Path())
def ep(src, dst, minify):
    """
    Transform an XML-formatted EP file into a JSON Patch.

    <SRC> must be a valid XML file containing the definition of an Extension
    Pack. <DST> is the final path of the result JSON Patch.
    """
    root = read_xml_ep(src)
    ep = xml_to_extension_pack(root)
    patch = extension_pack_to_json_patch(ep).to_string()
    with open(dst, "w") as f:
        f.write(json.dumps(json.loads(patch), indent=JSON_INDENT))
        print("-- Written to '{}'".format(dst))
