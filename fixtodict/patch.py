from jsonpatch import JsonPatch
from jsonschema import validate

from .resources import JSON_SCHEMA_V1


def apply_patch(data, patch: JsonPatch):
    validate(data, JSON_SCHEMA_V1)
    data = patch.apply(data, in_place=True)
    # TODO: meta and history stuff.
    return data
