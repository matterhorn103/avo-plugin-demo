# SPDX-License-Identifier: BSD 3-Clause
"""A command that moves all atoms 1 angstrom in the x direction."""

import argparse
import json
import sys


def move_atoms(cjson: dict, atoms: list[int]):
    # The coordinates are a simple list i.e. [x0, y0, z0, x1, y1, z1, x2, …]
    # so the x-coordinate of atom n is at index 3n
    for n in atoms:
        cjson["atoms"]["coords"]["3d"][n * 3] += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", nargs="?", default="en")
    args = parser.parse_args()

    # Read input from Avogadro
    avo_input = json.load(sys.stdin)
    cjson = avo_input["cjson"]
    # Get selected atoms
    selected = []
    selected_flags = cjson["atoms"]["selected"]  # 1 for selected, 0 for not
    n_atoms = len(selected_flags)
    for i, status in enumerate(selected_flags):
        if status == 1:
            selected.append(i)
    # If nothing is selected, move everything
    if len(selected) == 0:
        n_atoms = len(cjson["atoms"]["elements"]["number"])
        selected = list(range(n_atoms))

    # Make the change
    move_atoms(cjson, atoms=selected)
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
