# SPDX-License-Identifier: BSD 3-Clause
"""Generate input for the (fictional) Quantum Avocado program, whose syntax is
similar to that of Q-Chem."""

import argparse
import json
import sys


def generate_input_file(opts) -> str:
    # Extract options:
    title = opts["Title"]
    calc = opts["Calculation Type"]
    theory = opts["Theory"]
    basis = opts["Basis"]
    charge = opts["Charge"]
    multiplicity = opts["Multiplicity"]

    # Convert to code-specific strings
    if calc == "Single Point":
        calc_str = "SP"
    elif calc == "Equilibrium Geometry":
        calc_str = "Opt"
    elif calc == "Frequencies":
        calc_str = "Freq"
    else:
        raise Exception(f"Unhandled calculation type: {calc}")

    if theory in ["HF", "B3LYP", "B3LYP5", "EDF1", "M062X", "MP2", "CCSD"]:
        theory_str = theory
    else:
        raise Exception(f"Unhandled theory type: {theory}")

    if basis in [
        "STO-3G",
        "3-21G",
        "6-31G(d)",
        "6-31G(d,p)",
        "6-31+G(d)",
        "6-311G(d)",
        "cc-pVDZ",
        "cc-pVTZ",
    ]:
        basis_str = f"BASIS {basis}"
    elif basis in ["LANL2DZ", "LACVP"]:
        basis_str = f"ECP {basis}"
    else:
        raise Exception(f"Unhandled basis type: {basis}")

    output = [
        "$rem",
        f"   JOBTYPE {calc_str}",
        f"   METHOD {theory_str}",
        f"   {basis_str}",
        "   GUI 2",
        "$end",
        "",  # Empty line
        "$comment",
        f"   {title}",
        "$end",
        "",
        "$molecule",
        f"   {charge} {multiplicity}",
        "$$coords:___Sxyz$$",
        "$end",
        "",
    ]

    return "\n".join(output)


def generate_files(data: dict) -> dict:

    # Generate the input file
    input_file = generate_input_file(data["options"])

    # Get the basename for input files:
    basename = data["options"]["Filename Base"]

    # Prepare the result
    result = {
        # Text of the input files generated
        # If multiple have been generated they will appear in the same order in
        # the GUI as they are listed in this array
        "files": [
            {"filename": f"{basename}.qcin", "contents": input_file}
        ],
        # The main input file
        "mainFile": f"{basename}.qcin",
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", nargs="?", default="en")
    parser.add_argument("--debug", action="store_true")
    # If we had specified in `avogadro.toml` that the user options should be
    # obtained dynamically, we would have to also handle the flag for it
    #parser.add_argument("--user-options")
    args = parser.parse_args()

    avo_input = json.load(sys.stdin)

    try:
        output = generate_files(avo_input)
    # If there's a problem, let it be shown to the user as a warning
    except Exception as e:
        result = {
            "warnings": [str(e)],
        }
    
    print(json.dumps(output))
