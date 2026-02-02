# SPDX-License-Identifier: BSD 3-Clause
"""A menu command that causes a "Hello World!" message to be displayed to the
user."""

import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--lang", nargs="?", default="en")
    args = parser.parse_args()

    # Always have to read input from Avogadro and pass cjson back
    # Otherwise molecule disappears
    avo_input = json.loads(args.input)

    # Extract number of times to shout hello from user's config
    n_hello = avo_input["config"]["hello_repeats"]

    # Send the user a message that will appear in a pop-up dialog
    message = "Hello World!\n" * n_hello

    # Assemble output
    output = {
        "message": message,
        "moleculeFormat": "cjson",
        "cjson": avo_input["cjson"],
    }

    # Pass back to Avogadro
    print(json.dumps(output))
