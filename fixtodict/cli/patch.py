import click
import json
import jsonpatch

from ..utils import read_json, DEFAULT_INDENT
from . import cli


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("patch", nargs=1, type=click.Path(exists=True))
def patch(src, patch):
    """
    Apply a JSON Patch file.
    """
    data = read_json(src)
    patch = jsonpatch.JsonPatch(read_json(patch))
    data = patch.apply(data)
    data_json = json.dumps(data, indent=DEFAULT_INDENT)
    print(data_json)
