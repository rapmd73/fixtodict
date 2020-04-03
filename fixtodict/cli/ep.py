import click

from . import cli
from .utils.xml import read_xml_ep
from .utils.json import beautify_json
from ..extension_pack import ExtensionPack


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("dst", nargs=1, type=click.Path())
def ep(src, dst, improve_docs):
    """
    Transform an XML-formatted EP file into a JSON Patch.

    <SRC> must be a valid XML file containing the definition of an Extension
    Pack. <DST> is the final path of the result JSON Patch.
    """
    root = read_xml_ep(src)
    patch = ExtensionPack(root).to_jsonpatch().to_string()
    with open(dst, "w") as f:
        f.write(beautify_json(patch))
        print("-- Written to '{}'".format(dst))
