# SPDX-License-Identifier: BSD 3-Clause
"""Generate input for the (fictional) Quantum Avocado program, whose syntax is
similar to that of Q-Chem."""

import argparse
import json


def generate_input_file(opts):
    # Extract options:
    title = opts["title"]
    calc = opts["calc_type"]
    theory = opts["theory"]
    basis = opts["basis"]
    charge = opts["charge"]
    multiplicity = opts["multiplicity"]

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


def generate_files(data: dict):

    # Generate the input file
    input_file = generate_input_file(data["options"])

    # Get the basename for input files:
    basename = data["options"]["filename_base"]

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
    parser.add_argument("input")
    parser.add_argument("--lang", nargs="?", default="en")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    try:
        output = generate_files(args.input)
        print(json.dumps(output))
    except Exception as e:
        # If there's an error, let it be shown to the user
        print(e)
