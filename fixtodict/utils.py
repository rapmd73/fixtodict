import os
import datetime


def filter_none(data):
    return {k: v for k, v in data.items() if v is not None}


def iso8601_local():
    # <https://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-doesnt-include-z-zulu-or-zero-offset>
    return datetime.datetime.now().replace(microsecond=0).isoformat() + "Z"
