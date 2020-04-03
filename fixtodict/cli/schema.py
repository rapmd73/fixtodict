from . import cli
from ..schema import JSON_SCHEMA_V1


@cli.command()
def schema():
    """
    Print the JSON Schema used by FIXtodict.
    """
    print(JSON_SCHEMA_V1)
