import argparse
import glob
import os
from converter import Converter, LocalTester

def convert_master(scandir):
    if scandir is None:
        scandir = os.getcwd()
    if not os.path.exists(scandir):
        print(f"Directory not found: {scandir}")
        return
    os.chdir(scandir)
    flist = glob.glob("*_master.py")
    if len(flist) == 0:
        print(f"No file named *_master.py in directory: {scandir}")
        return
    file = os.path.join(scandir, flist[0])
    conv = Converter(file)
    conv.convert()
    tester = LocalTester(scandir)
    tester.prepare()
    tester.run_local_tests()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scandir", help="directory containing *_master.py file")
    args = parser.parse_args()
    convert_master(args.scandir)
