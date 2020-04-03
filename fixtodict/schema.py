import pkg_resources
import json
import jsonschema

JSON_SCHEMA_V1 = pkg_resources.resource_string(
    "fixtodict", "resources/schema/v1.json"
).decode("ascii")


def validate_v1(data):
    jsonschema.validate(data, json.loads(JSON_SCHEMA_V1))