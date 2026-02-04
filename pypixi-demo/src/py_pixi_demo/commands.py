# SPDX-License-Identifier: BSD 3-Clause
"""The various menu commands defined by the plugin, all in one place."""


def hello_world(avo_input: dict) -> dict:
    """A menu command that causes a "Hello World!" message to be displayed to the
    user."""

    # Extract number of times to shout hello from user's config
    n_hello = avo_input["config"]["hello_repeats"]

    # Send the user a message that will appear in a pop-up dialog
    message = "Hello World!\n" * n_hello

    # Assemble output
    # Always have to pass the cjson back, otherwise the molecule disappears
    output = {
        "message": message,
        "moleculeFormat": "cjson",
        "cjson": avo_input["cjson"],
    }

    return output


def move_atoms(cjson: dict, atoms: list[int]):
    """A command that moves the specified atoms 1 angstrom in the x direction."""
    # The coordinates are a simple list i.e. [x0, y0, z0, x1, y1, z1, x2, …]
    # so the x-coordinate of atom n is at index 3n
    for n in atoms:
        cjson["atoms"]["coords"]["3d"][n * 3] += 1


def do_move(avo_input: dict, move_all: bool) -> dict:
    cjson = avo_input["cjson"]

    if move_all:
        # Get selected atoms
        selected = []
        selected_flags = cjson["atoms"]["selected"]  # 1 for selected, 0 for not
        n_atoms = len(selected_flags)
        for i, status in enumerate(selected_flags):
            if status == 1:
                selected.append(i)
        # If nothing is selected, move everything
        if len(selected) == 0:
            n_atoms = len(cjson["atoms"]["elements"]["number"])
            selected = list(range(n_atoms))
    else:
        selected = list(avo_input["options"]["selection"])
    
    # Make the appropriate changes
    move_atoms(cjson, selected)
    # Be careful, because the atoms' positions have now been changed in the
    # original data (`avo_input`) too!
    # Often, you will want to avoid this by using `deepcopy()`

    # Assemble output
    output = {
        "moleculeFormat": "cjson",
        "cjson": cjson,
    }

    return output


def do_alchemy(avo_input: dict) -> dict:
    """A command that turns all metal (in the astronomer's sense) into gold."""
    cjson = avo_input["cjson"]
    for i, z in enumerate(cjson["atoms"]["elements"]["number"]):
        if z > 2:
            cjson["atoms"]["elements"]["number"][i] = 79
    output = {
        "moleculeFormat": "cjson",
        "cjson": cjson,
    }
    return output
