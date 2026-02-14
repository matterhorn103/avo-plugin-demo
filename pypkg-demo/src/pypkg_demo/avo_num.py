# SPDX-License-Identifier: BSD 3-Clause
"""Assign atomic partial charges according to the digits of Avogadro's number."""


def charges(cjson: dict) -> dict:
    # Since we are assigning the charges arbitrarily we only need to know the
    # number of atoms for our example, the rest of the input is irrelvant

    n_atoms = len(cjson["atoms"]["elements"]["number"])

    digits = [6, 0, 2, 2, 1, 4, 0, 7, 6]

    charges = []
    for i in range(n_atoms):
        # Return alternating positive and negative charges so that the net
        # charge is either 0 or small
        magnitude = digits[i // 2] / 10
        if i % 2 == 0:
            charges.append(magnitude)
        else:
            charges.append(-magnitude)

    output = {
        "charges": charges
    }
    
    return output


def potential():
    # The plugin has stated in pyproject.toml that potentials are not supported
    # so this method should never be necessary anyway

    return {}


if __name__ == "__main__":
    input = {
        "atoms": {
            "elements": {
                "number": [
                    1, 2, 3, 4, 5, 6,
                ]
            }
        }
    }
    print(charges(input))
