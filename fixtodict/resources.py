import pkg_resources
import json
import os
from xml.etree import ElementTree

PKG_NAME = "fixtodict"

LEGAL_INFO = (
    'FIXtodict is distributed on an "AS IS" BASIS, '
    "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, "
    "either express or implied."
)

JSON_SCHEMA = pkg_resources.resource_string(
    PKG_NAME, "resources/schema/v1.json"
).decode("ascii")


def test_cases(tag):
    data = []
    t_cases = pkg_resources.resource_listdir(
        PKG_NAME, "tests/resources/{}/".format(tag)
    )
    for t_case in t_cases:
        base, extension = os.path.splitext(t_case)
        if extension == ".xml":
            xml_string = pkg_resources.resource_string(
                PKG_NAME, "tests/resources/{}/{}.xml".format(tag, base)
            )
            json_string = pkg_resources.resource_string(
                PKG_NAME, "tests/resources/{}/{}.json".format(tag, base)
            )
            data.append(
                (ElementTree.fromstring(xml_string), json.loads(json_string))
            )
    return data
