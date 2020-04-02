import os
import datetime
import json
from xml.etree import ElementTree
from typing import List

DEFAULT_INDENT = 2


def parse_protocol_version(val: str, ep=None):
    if "_EP" in val:
        val, ep = tuple(val.split("_EP"))
    if "SP" in val:
        val, sp = tuple(val.split("SP"))
    else:
        sp = "0"
    protocol, major, minor = tuple(val.split("."))
    protocol = protocol.lower()
    data = {
        "fix": protocol,
        "major": major,
        "minor": minor,
        "sp": sp,
    }
    if ep:
        data["ep"] = ep
    return data


def version_from_xml_attrs(d: dict, prefix="added"):
    main = prefix
    ep = prefix + "EP"
    if main in d and ep in d and d[ep] != "-1":
        return parse_protocol_version(d[main], d[ep])
    elif main in d:
        return parse_protocol_version(d[main])
    else:
        return None


def target_filename(target_dir, v, ext="json"):
    return os.path.join(
        target_dir,
        "{}-{}-{}{}.{}".format(v["fix"], v["major"], v["minor"],
                               "-sp" + v["sp"] if v["sp"] != "0" else "", ext))


def iso8601_local():
    # <https://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-doesnt-include-z-zulu-or-zero-offset>
    return datetime.datetime.now().replace(microsecond=0).isoformat() + "Z"

# ------
# I/O
# ------


def err(path, extension):
    print("Error: Invalid {} file.".format(extension))
    exit(-1)


def read_xml_root(src, filename, opt=True):
    path = os.path.join(src, filename)
    try:
        return ElementTree.parse(path).getroot()
    except:
        if not opt:
            err(path, "XML")
    return None


def read_xml_ep(path):
    try:
        return ElementTree.parse(path).getroot()
    except:
        err(path, "XML")


def read_json(path):
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except:
        err(path, "JSON")
