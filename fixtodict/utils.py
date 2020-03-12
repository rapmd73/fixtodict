import os
import datetime
from typing import List


def parse_protocol_version(val: str, ep: str = "-1"):
    """
    Parses a string that represents a FIX protocol version into its original
    fields.
    """
    # Explicit servicepack tagging.
    if "SP" in val:
        protocol, servicepack = tuple(val.split("SP"))
    else:
        protocol, servicepack = val, "0"
    protocol, major, minor = tuple(protocol.split("."))
    protocol = protocol.lower()
    if ep == "-1":
        return [protocol, major, minor, servicepack]
    else:
        return [protocol, major, minor, servicepack, ep]


def protocol_from_xml_attrs(d: dict):
    if "addedEP" in d:
        return parse_protocol_version(d["added"], d["addedEP"])
    else:
        return parse_protocol_version(d["added"])


def target_filename(target_dir, version: str):
    v_fields = parse_protocol_version(version)
    return os.path.join(
        target_dir, "{}-{}-{}{}.json".format(
            v_fields[0], v_fields[1], v_fields[2],
            "-sp" + v_fields[3] if v_fields[3] != "0" else ""))


def iso8601_local():
    # <https://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-doesnt-include-z-zulu-or-zero-offset>
    return datetime.datetime.now().replace(microsecond=0).isoformat() + "Z"
