# SPDX-License-Identifier: BSD 3-Clause
"""A command that moves a user-specified atom 1 angstrom in the x direction."""

import argparse
import json
import sys


def move_atom(cjson: dict, atom: int):
    # The coordinates are a simple list i.e. [x0, y0, z0, x1, y1, z1, x2, …]
    # so the x-coordinate of atom n is at index 3n
    cjson["atoms"]["coords"]["3d"][atom * 3] += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", nargs="?", default="en")
    args = parser.parse_args()

    # Read input from Avogadro
    avo_input = json.load(sys.stdin)
    cjson = avo_input["cjson"]
    requested_atom = avo_input["options"]["selection"]

    # Make the change
    move_atom(cjson, requested_atom)
    # Be careful, because the atom's position has now been changed in the
    # original data (`avo_input`) too!
    # Often, you will want to avoid this by using `deepcopy()`

    # Assemble output
    output = {
        "moleculeFormat": "cjson",
        "cjson": cjson,
    }

    # Pass back to Avogadro
    print(json.dumps(output))
