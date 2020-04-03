import os


class FixVersion:
    def __init__(self, val: str, ep=None):
        if "_EP" in val:
            val, ep = tuple(val.split("_EP"))
        if "SP" in val:
            val, sp = tuple(val.split("SP"))
        else:
            sp = "0"
        protocol, major, minor = tuple(val.split("."))
        protocol = protocol.lower()
        self.data = {
            "fix": protocol,
            "major": major,
            "minor": minor,
            "sp": sp,
        }
        if ep:
            self.data["ep"] = ep

    @classmethod
    def create_from_xml_attrs(d, prefix="added"):
        main = prefix
        ep = prefix + "EP"
        if main in d and ep in d and d[ep] != "-1":
            return Version(d[main], d[ep])
        elif main in d:
            return Version(d[main])
        else:
            return None
