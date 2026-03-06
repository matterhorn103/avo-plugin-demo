"""A function to interpret the arguments passed to the plugin."""

import json
import sys
import traceback

def run(args):
    # The input for all feature types is passed as JSON on `stdin`
    # This is easily parsed into a native Python `dict`
    avo_input = json.load(sys.stdin)
    output = None
    # Do everything in one big try block so that if an exception occurs we can
    # catch it and report back to the user
    try:
        match args.feature:
            # A large plugin can run faster if we only import the necessary feature
            case "avogadro_charges":
                from .avo_num import charges, potential
                if args.charges:
                    output = charges(avo_input["cjson"])
                else:
                    output = potential()
            case "stellar":
                from .stellar import run
                run(avo_input["cjson"])
            case "zyx":
                from .zyx import read, write
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
            case "qavocado":
                from .qavocado import generate_files
                output = generate_files(avo_input)
            case "hello":
                from .commands import hello_world
                output = hello_world(avo_input)
            case "transmute":
                from .commands import do_alchemy
                output = do_alchemy(avo_input)
            # Handle the move commands together
            case "moveatom" | "moveall":
                from .commands import do_move
                output = do_move(
                    avo_input, move_all=(args.feature == "moveall"),
                )
    except Exception as e:
        if args.debug:
            output = {"error": traceback.format_exception(e)}
        else:
            output = {"error": str(e)}    
    if output is not None:
        # Pass back to Avogadro
        print(json.dumps(output))
