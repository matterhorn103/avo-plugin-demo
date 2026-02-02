# SPDX-License-Identifier: BSD 3-Clause
"""A command that moves all atoms 1 angstrom in the x direction."""

import argparse
import json


def move_atoms(cjson: dict):
    # The coordinates are a simple list i.e. [x0, y0, z0, x1, y1, z1, x2, …]
    # so the x-coordinates of atoms n are at index 3n
    n_atoms = len(cjson["atoms"]["elements"]["number"])
    for n in range(n_atoms):
        cjson["atoms"]["coords"]["3d"][n * 3] += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--lang", nargs="?", default="en")
    args = parser.parse_args()

    # Read input from Avogadro
    avo_input = json.loads(args.input)
    cjson = avo_input["cjson"]
    requested_atom = avo_input["options"]["selection"]

    # Make the change
    move_atoms(cjson)
    # Be careful, because the atoms' positions have now been changed in the
    # original data (`avo_input`) too!
    # Often, you will want to avoid this by using `deepcopy()`

    # Assemble output
    output = {
        "moleculeFormat": "cjson",
        "cjson": cjson,
    }

    # Pass back to Avogadro
    print(json.dumps(output))
