import argparse
from converter import Converter

def convert_master(scandir, action = "all"):
    conv = Converter(scandir)
    if action != "test":
        conv.convert()
    if action != "convert":
        conv.run_local_tests()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scandir", help="directory containing *_master.py file")
    parser.add_argument("--action", choices=["all", "convert", "test"], default="all", help="run converter, run tests or all")
    args = parser.parse_args()
    convert_master(args.scandir, args.action)
