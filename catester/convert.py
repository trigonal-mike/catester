import argparse
from converter import Converter

def convert_master(scandir, action="all", verbosity=0, metayaml=None):
    conv = Converter(scandir, metayaml)
    if action in [None, "all", "cleanup"]:
        conv.cleanup()
    if action in [None, "all", "convert"]:
        conv.convert()
    if action in [None, "all", "test"]:
        conv.run_local_tests(verbosity)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scandir", help="directory containing *_master.py file")
    parser.add_argument("--action", choices=["all", "cleanup", "convert", "test"], default="all", help="run converter, run tests or all")
    parser.add_argument("--verbosity", default=0, help="verbosity level 0, 1, 2 or 3")
    parser.add_argument("--metayaml", default=None, help="abs/rel path to initial meta.yaml")
    args = parser.parse_args()
    convert_master(args.scandir, args.action, args.verbosity, args.metayaml)
