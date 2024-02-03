import argparse
import glob
import os
from converter import Converter, LocalTester

def convert_master(scandir, action:str = "all"):
    if scandir is None:
        scandir = os.getcwd()
    if not os.path.exists(scandir):
        print(f"Directory not found: {scandir}")
        return
    os.chdir(scandir)
    if action != "test":
        flist = glob.glob("*_master.py")
        if len(flist) == 0:
            print(f"No file named *_master.py in directory: {scandir}")
            return
        file = os.path.join(scandir, flist[0])
        conv = Converter(file)
        conv.convert()
    if action != "convert":
        tester = LocalTester(scandir)
        tester.prepare()
        tester.run_local_tests()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scandir", help="directory containing *_master.py file")
    parser.add_argument("--action", choices=["all", "test", "convert"], default="all", help="run converter, run tests or all")
    args = parser.parse_args()
    convert_master(args.scandir, args.action)
