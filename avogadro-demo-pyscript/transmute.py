# SPDX-License-Identifier: BSD 3-Clause
"""A command that turns all metal (in the astronomer's sense) into gold."""

import argparse
import json
import sys


def do_alchemy(cjson: dict):
    for i, z in enumerate(cjson["atoms"]["elements"]["number"]):
        if z > 2:
            cjson["atoms"]["elements"]["number"][i] = 79


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", nargs="?", default="en")
    args = parser.parse_args()

    # Read input from Avogadro
    avo_input = json.load(sys.stdin)
    cjson = avo_input["cjson"]
    requested_atom = avo_input["options"]["selection"]

    # Make the changes
    do_alchemy(cjson)
    # Be careful, because the elements have now been changed in the
    # original data (`avo_input`) too!
    # Often, you will want to avoid this by using `deepcopy()`

    # Assemble output
    output = {
        "moleculeFormat": "cjson",
        "cjson": cjson,
    }

    # Pass back to Avogadro
    print(json.dumps(output))
