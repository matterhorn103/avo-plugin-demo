"""Defines an entry point for the plugin for Avogadro to call."""

import argparse

from .run import run

def main():
    # This is the entry point that we have defined as such in `pyproject.toml`
    # and is the function that will be run when Avogadro invokes the plugin

    # Avogadro will call the plugin with the identifier of the feature in
    # question as the main argument, followed by specific arguments and flags
    # for the feature

    # The plugin may parse the command passed by Avogadro however it likes, and
    # with whichever parsing library, but this is perhaps the easiest

    # First we create a main parser
    parser = argparse.ArgumentParser()
    # We can capture common shared arguments immediately for all features
    parser.add_argument("--lang", nargs="?", default="en")
    parser.add_argument("--debug", action="store_true")

    # If our plugin only provided one type of feature, we could capture all the
    # arguments at this point, because they'd be the same for all features, and
    # we'd capture the feature identifier using
    #parser.add_argument("feature")

    # When the args for each feature differ, we have to delegate to subparsers
    subparsers = parser.add_subparsers(dest="feature")
    # Each feature gets its own subparser, where the `title` of each
    # subparser must match the `identifier` for the feature
    # We then add the arguments specific to each feature to its subparser

    parser_charges = subparsers.add_parser("avogadro_charges")
    parser_charges.add_argument("input")
    parser_charges.add_argument("--charges", action="store_true")
    parser_charges.add_argument("--potential", action="store_true")

    parser_energy = subparsers.add_parser("stellar")
    parser_energy.add_argument("input")

    parser_format = subparsers.add_parser("zyx")
    parser_format.add_argument("input")
    parser_format.add_argument("--read", action="store_true")
    parser_format.add_argument("--write", action="store_true")

    parser_generator = subparsers.add_parser("qavocado")
    parser_generator.add_argument("input")
    # If we had specified in `pyproject.toml` that the user options should be
    # obtained dynamically, we would have to also handle the flag for it
    #parser_generator.add_argument("--print-options")

    parser_transmute = subparsers.add_parser("transmute")
    parser_transmute.add_argument("input")

    parser_moveatom = subparsers.add_parser("moveatom")
    parser_moveatom.add_argument("input")

    parser_moveall = subparsers.add_parser("moveall")
    parser_moveall.add_argument("input")

    parser_hello = subparsers.add_parser("hello")
    parser_hello.add_argument("input")
    
    # Now the parser knows what to expect, we actually parse the command
    args = parser.parse_args()
    # Regardless of whether subparsers were used or not, the feature that has
    # been invoked is now stored as `args.feature`, and the other arguments have
    # been parsed as appropriate for the invoked feature

    # The plugin is now free to handle everything however it likes
    # Some may prefer to do more right here, some may prefer to only do argument
    # parsing at the entry point

    # Here, we've kept this file dedicated to defining the entry point and
    # parsing the args, with the interpretation of the arguments delegated to
    # another function in another module
    run(args)
