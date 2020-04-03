from ...fix_version import FixVersion


def err(extension):
    print("Error: Invalid {} file.".format(extension))
    exit(-1)


def derive_target_filename(v: FixVersion, target_dir, ext="json"):
    return os.path.join(
        target_dir,
        "{}-{}-{}{}.{}".format(
            v["fix"],
            v["major"],
            v["minor"],
            "-sp" + v["sp"] if v["sp"] != "0" else "",
            ext,
        ),
    )
