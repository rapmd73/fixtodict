from jsonpatch import JsonPatch

from .schema import validate_v1


def apply_patch(data, patch: JsonPatch):
    validate_v1(data)
    data = patch.apply(data, in_place=True)
    # TODO: meta and history stuff.
    return data
