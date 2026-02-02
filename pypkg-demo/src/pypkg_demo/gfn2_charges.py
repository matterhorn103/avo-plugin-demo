# SPDX-License-Identifier: BSD 3-Clause
"""Calculate atomic partial charges using a local installation of xtb."""

import sys
import os
from shutil import which
import tempfile
import subprocess


def charges():
    # Avogadro will send us the mol file as stdin
    # we need to write it to a temporary file

    # get the whole file
    mol = sys.stdin.read()

    fd, name = tempfile.mkstemp(".sdf")
    os.write(fd, mol.encode())
    os.close(fd)

    # get the total charge and spin from the input
    # i.e., read the line after <AVOGADRO_TOTAL_CHARGE>
    # and the line after <AVOGADRO_TOTAL_SPIN>
    charge = 0
    spin = 1
    read_charge = False
    read_spin = False
    # iterate through the lines in mol
    for line in mol.splitlines():
        if "<AVOGADRO_TOTAL_CHARGE>" in line:
            read_charge = True
            continue
        if "<AVOGADRO_TOTAL_SPIN>" in line:
            read_spin = True
            continue
        if read_charge:
            charge = int(line.strip())
            read_charge = False
            continue
        if read_spin:
            spin = int(line.strip())
            read_spin = False
            continue

    # run xtb
    xtb = which("xtb")
    if xtb is None:
        # Can't work if xtb is missing!
        raise Exception("Local installation of xtb not found!")

    # for now, ignore the output itself
    tempdir = tempfile.mkdtemp()
    arguments = [xtb, name, "--gfn2", "--chrg", str(charge)]
    if spin != 1:
        arguments.append("--uhf")
        arguments.append(str(spin - 1))
    output = subprocess.run(
        arguments, stdout=subprocess.PIPE, cwd=tempdir, check=True
    )
    # instead we read the "charges" file
    result = ""
    with open(tempdir + "/" + "charges", "r", encoding="utf-8") as f:
        result = f.read()

    # try to cleanup the temporary files
    os.remove(name)
    for filename in os.listdir(tempdir):
        try:
            os.remove(tempdir + "/" + filename)
        except:
            continue
    # and try to cleanup the directory
    try:
        os.rmdir(tempdir)
    except:
        pass

    # write the charges to stdout
    return result


def potential():
    # at the moment, xtb doesn't have a good way to do this
    # and the method shouldn't be called anyway

    return ""
