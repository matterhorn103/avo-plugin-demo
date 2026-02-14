"""A function to interpret the arguments passed to the plugin."""

import json

def run(args):
    avo_input = json.loads(args.input)
    output = None
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
            try:
                from .qavocado import generate_files
                # Parse the JSON strings
                data = json.loads(args.input)
                output = generate_files(data)
            except Exception as e:
                # If there's an error, let it be shown to the user
                print(e)
        # commands all receive a JSON as input, and we've asked
        # (in `pyproject.toml`) for a CJSON in all cases
        # They also all return a JSON as output, so let's handle them together
        case _:
            from .commands import do_alchemy, do_move, hello_world
            cjson = avo_input["cjson"]
            match args.feature:
                case "transmute":
                    output = do_alchemy(cjson)
                # Handle the move commands together
                case "moveatom" | "moveall":  
                    output = do_move(avo_input, move_all=(args.feature == "moveall"))
                case "hello":
                    output = hello_world(avo_input)
    if output is not None:
        # Pass back to Avogadro
        print(json.dumps(output))
