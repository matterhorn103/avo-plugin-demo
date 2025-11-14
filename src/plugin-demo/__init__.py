import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", action="store")
    parser.add_argument("--print-options", action="store_true")
    parser.add_argument("--lang", nargs="?", default="en")
    args = parser.parse_args()
