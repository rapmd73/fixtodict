import click
import jsonpatch
import json

from . import cli
from .utils.xml import read_xml_root
from .utils.json import read_json, DEFAULT_INDENT
from ..repository import transform_orchestra_v1


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
def o_repo(src):
    root = read_xml_root("", src, opt=False)
    data = transform_orchestra_v1(root)
    print(json.dumps(data, indent=DEFAULT_INDENT))
