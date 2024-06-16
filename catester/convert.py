import argparse
from converter import Converter

def convert_master(scandir, testrunnerdir, assignmentsdir, action="all", verbosity=0, pytestflags="", metayaml=None, formatter=True):
    conv = Converter(scandir, testrunnerdir, assignmentsdir, action, verbosity, pytestflags, metayaml, formatter)
    conv.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scandir", help="directory containing *_master.py file")
    parser.add_argument("--testrunnerdir", help="directory for local test runs")
    parser.add_argument("--assignmentsdir", help="directory containing assignments")
    parser.add_argument("--action", choices=["all", "cleanup", "convert", "test"], default="all", help="run converter, run tests or all")
    parser.add_argument("--verbosity", default=0, help="catester-verbosity level 0, 1, 2 or 3")
    parser.add_argument("--pytestflags", default="-ra,--tb=no", help="comma-separated flags, for configuring pytest")
    parser.add_argument("--metayaml", default=None, help="abs/rel path to initial meta.yaml")
    parser.add_argument("--formatter", action='store_true', help="use black as formatter for the reference-file")
    args = parser.parse_args()
    convert_master(args.scandir, args.testrunnerdir, args.assignmentsdir, args.action, args.verbosity, args.pytestflags, args.metayaml, args.formatter)
