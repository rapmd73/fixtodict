import click
import json
import jsonpatch

from . import cli
from .utils.json import read_json, DEFAULT_INDENT


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("path-to-patch", nargs=1, type=click.Path(exists=True))
def patch(src, path_to_patch):
    """
    Apply a JSON Patch file.
    """
    patch = jsonpatch.JsonPatch(read_json(path_to_patch))
    data = read_json(src)
    data_patched = patch.apply(data, in_place=True)
    print(json.dumps(data_patched, indent=DEFAULT_INDENT))
