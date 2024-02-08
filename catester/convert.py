import argparse
from converter import Converter

def convert_master(scandir, action="all", verbosity=0):
    conv = Converter(scandir)
    if action != "test":
        conv.convert()
    if action != "convert":
        conv.run_local_tests(verbosity)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scandir", help="directory containing *_master.py file")
    parser.add_argument("--action", choices=["all", "convert", "test"], default="all", help="run converter, run tests or all")
    parser.add_argument("--verbosity", default=0, help="verbosity level 0, 1, 2 or 3")
    args = parser.parse_args()
    convert_master(args.scandir, args.action, args.verbosity)
