import json

from . import err

DEFAULT_INDENT = 2


def beautify_json(json_string: str):
    return json.dumps(json.loads(json_string), indent=DEFAULT_INDENT)


def read_json(path):
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except json.JSONDecodeError:
        err("JSON")
