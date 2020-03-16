import click

from ..version import __version__


@click.group(name="FIXtodict")
@click.version_option(__version__)
def cli():
    """
    Easy and effective tooling for FIX Repository data.

    FIXtodict greatly simplifies working with FIX Repository data by
    leveraging open and combat-proven web technologies. The ultimate
    goal is to provide users with a consistent, authoritative and
    high-quality FIX reference in an accessible way. JSON is the preferred
    choice of format; JSON Schema [1] and JSON Patch [2] are internally used
    respectively for validation and Extension Packs (EPs).

    Type 'fixtodict <SUBCOMMAND> --help' for more information.

    \b
    Footnotes:
    [1]: https://json-schema.org/
         https://json-schema.org/draft/2019-09/json-schema-core.html
    [2]: https://tools.ietf.org/html/rfc6902

    \b
    Copyright (c) 2020, Filippo Costa. Released under Apache License 2.0:
      https://www.apache.org/licenses/LICENSE-2.0.txt
    Find me at <https://filippocosta.net>.
    """
    pass