import click
import json

from ..utils import read_json
from ..resources import JSON_SCHEMA
from . import cli
from jsonschema import validate as validate_schema


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
def validate(src):
    """
    Check a JSON file for correctness.
    """
    data = read_json(src)
    schema = json.loads(JSON_SCHEMA())
    validate_schema(instance=data, schema=schema)
