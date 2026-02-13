# SPDX-License-Identifier: BSD 3-Clause
"""Produce an energy related to the distance from the geometric centre."""

import json
import numpy as np


def energy(coords: np.ndarray, centre: np.ndarray, supernova: bool) -> float:
    # Simply treat as a repulsive or attractive force between each
    # atom and the centre
    # The energy contribution of each atom is either proportional or inversely
    # proportional to the square of its distance from the centre
    distances = np.linalg.norm(coords - centre, axis=1)
    # We'll arbitrarily make the optimized energy 1000 kJ mol-1 per atom
    asymptote = 1000.0
    if supernova:
        energies = (1/distances**2) - asymptote
    else:
        energies = distances**2 - asymptote

    energy = np.sum(energies)

    return energy


def run(cjson: dict):
    # Initial geometry is provided in CJSON format by Avogadro
    # Extract the coordinates into a numpy ndarray
    flat_coords = cjson["atoms"]["coords"]["3d"]
    # Use -1 as the array length to have it automatically adapt to the number of atoms 
    coords = np.array(flat_coords, dtype=float).reshape(-1, 3)

    # Work out the centre of the molecule
    centre = np.mean(coords, axis=0)

    # Check to see if the molecule has any atoms heavier than iron
    elements = cjson["atoms"]["elements"]["number"]
    n_atoms = len(elements)
    # Let's explode the molecule if it's heavy, otherwise have it collapse
    if max(elements) > 26:
        supernova = True
    else:
        supernova = False

    # Get initial energy for Avogadro (in kJ mol-1)
    initial_energy = energy(coords, centre, supernova)

    # Return the initial energy to Avogadro as a JSON
    # We could also send back an error message at this point if we wanted
    output = {"energy": initial_energy}
    print(json.dumps(output))

    # Now we look for updated coordinates on `stdin` from Avogadro, and return
    # the updated energy on `stdout`
    # We loop forever - Avogadro will kill the process when done
    while True:
        # Update the coordinates of the atoms
        for i in range(n_atoms):
            # The coordinates are passed as one line per atom, with the x, y,
            # and z coordinates separated by a single space
            coords[i] = np.fromstring(input(), sep=" ", dtype=float)
        new_energy = energy(coords, centre, supernova)
        # Print the updated energy
        print(f"energy: {new_energy}")
