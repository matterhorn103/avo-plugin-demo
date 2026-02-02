# SPDX-License-Identifier: BSD 3-Clause
""""Parser for a mostly useless file format consisting of xyz-style files but
with reversed coordinates."""

import argparse


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
    parser.add_argument("--read", action="store")
    parser.add_argument("--write", action="store")
    parser.add_argument("--lang", nargs="?", default="en")
    args = parser.parse_args()

    if args.read:
        print(read(args.read))
    elif args.write:
        print(write(args.write))
