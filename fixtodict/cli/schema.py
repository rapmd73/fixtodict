from . import cli
from ..resources import JSON_SCHEMA


@cli.command()
def schema():
    """
    Print the JSON Schema used by FIXtodict.
    """
    print(JSON_SCHEMA)
