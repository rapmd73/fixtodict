import click
import json
from jsonschema import validate as validate_schema

from . import cli
from .utils.json import read_json
from ..resources import JSON_SCHEMA


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
def validate(src):
    """
    Check a JSON file for correctness.
    """
    data = read_json(src)
    schema = json.loads(JSON_SCHEMA)
    validate_schema(instance=data, schema=schema)
