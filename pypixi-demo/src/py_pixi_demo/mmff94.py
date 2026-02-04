# SPDX-License-Identifier: BSD 3-Clause
"""Calculate the MMFF94 energy using Open Babel."""

import numpy as np
from openbabel import pybel


def run(cjson: str):
    # we get the molecule from the supplied filename
    #  in cjson format (it's a temporary file created by Avogadro)
    mol = next(pybel.readstring("cjson", cjson))

    ff = pybel._forcefields["mmff94"]
    success = ff.Setup(mol.OBMol)
    if not success:
        # should never happen, but just in case
        raise Exception("MMFF94 force field setup failed")

    # we loop forever - Avogadro will kill the process when done
    num_atoms = len(mol.atoms)
    while True:
        # read new coordinates from stdin
        for i in range(num_atoms):
            coordinates = np.fromstring(input(), sep=" ")
            atom = mol.atoms[i]
            atom.OBAtom.SetVector(coordinates[0], coordinates[1], coordinates[2])

        # update the molecule geometry for the next energy
        ff.SetCoordinates(mol.OBMol)

        # first print the energy of these coordinates
        energy = ff.Energy(True)  # in kJ/mol
        print("AvogadroEnergy:", energy)  # in kJ/mol

        # now print the gradient on each atom
        print("AvogadroGradient:")
        for atom in mol.atoms:
            grad = ff.GetGradient(atom.OBAtom)
            print(-1.0*grad.GetX(), -1.0*grad.GetY(), -1.0*grad.GetZ())
