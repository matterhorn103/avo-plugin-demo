# SPDX-License-Identifier: BSD 3-Clause
"""Parser for a mostly useless file format consisting of xyz-style files but
with reversed coordinates."""

import argparse
import json
import sys


def write(xyz: str) -> str:
    xyz_lines = xyz.splitlines()
    # Just copy the first two lines: numAtoms and comment/title
    zyx = xyz_lines[:2]

    for line in xyz_lines:
        parts = line.split()
        reversed_line = "    ".join([parts[0], parts[3], parts[2], parts[1]])
        if len(parts) > 4:
            reversed_line += parts[4:].join(" ")
        zyx.append(reversed_line)

    # Make sure the file finishes with a newline
    zyx.append("")

    return "\n".join(zyx)


def read(zyx: str) -> str:
    # Reading is in this case the exact same process as writing
    zyx_lines = zyx.splitlines()
    # Just copy the first two lines: numAtoms and comment/title
    xyz = zyx_lines[:2]

    for line in zyx_lines:
        parts = line.split()
        reversed_line = "    ".join([parts[0], parts[3], parts[2], parts[1]])
        if len(parts) > 4:
            reversed_line += parts[4:].join(" ")
        xyz.append(reversed_line)

    # Make sure the file finishes with a newline
    xyz.append("")

    return "\n".join(xyz)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--lang", nargs="?", default="en")
    parser.add_argument("--read", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    # Read input from Avogadro
    avo_input = json.load(sys.stdin)

    if args.read:
        xyz = read(avo_input["file"])
        output = {
            "files": [
                xyz,
            ]
        }
    elif args.write:
        zyx = write(avo_input["xyz"])
        output = {
            "files": [
                zyx,
            ]
        }
    print(json.dumps(output))
