import os
import datetime
from typing import List


def parse_protocol_version(val: str, ep=None):
    # Explicit servicepack tagging.
    if "_EP" in val:
        val, ep = tuple(val.split("_EP"))
    if "SP" in val:
        val, servicepack = tuple(val.split("SP"))
    else:
        servicepack = "0"
    protocol, major, minor = tuple(val.split("."))
    protocol = protocol.lower()
    return {
        "fix": protocol,
        "major": major,
        "minor": minor,
        "sp": servicepack,
        "ep": ep
    }


def version_from_xml_attrs(d: dict, prefix="added"):
    main = prefix
    ep = prefix + "EP"
    if main in d and ep in d:
        return parse_protocol_version(d[main], d[ep])
    elif main in d:
        return parse_protocol_version(d[main])
    else:
        return None


def target_filename(target_dir, v):
    return os.path.join(
        target_dir, "{}-{}-{}{}.json".format(
            v["fix"], v["major"], v["minor"],
            "-sp" + v["sp"] if v["sp"] != "0" else ""))


def iso8601_local():
    # <https://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-doesnt-include-z-zulu-or-zero-offset>
    return datetime.datetime.now().replace(microsecond=0).isoformat() + "Z"
