import pkg_resources
import json
import os
from xml.etree import ElementTree

JSON_SCHEMA = pkg_resources.resource_string(
    "fixtodict", "resources/schema/v1.json").decode("ascii")


def test_cases(tag):
    data = []
    t_cases = pkg_resources.resource_listdir(
        "fixtodict", "tests/resources/{}/".format(tag))
    for t_case in t_cases:
        base, extension = os.path.splitext(t_case)
        if extension == ".xml":
            xml_string = pkg_resources.resource_string(
                "fixtodict", "tests/resources/{}/{}.xml".format(tag, base))
            json_string = pkg_resources.resource_string(
                "fixtodict", "tests/resources/{}/{}.json".format(tag, base))
            data.append((
                ElementTree.fromstring(xml_string),
                json.loads(json_string)
            ))
    return data
