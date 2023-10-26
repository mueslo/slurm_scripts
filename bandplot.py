#!/usr/bin/env python3
import os
import argparse
from shutil import copy
import glob
import pyfplo.fedit as fedit
import subprocess

parser = argparse.ArgumentParser(
	description='Create and optionally queue bandplot calculation.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
parser.add_argument('directory', metavar='DIR', help='FPLO run directory', nargs='*')
parser.add_argument('--time', metavar='TIME', help='Requested time in hours', type=float, default=1)
parser.add_argument('--weights', help='Get bandweights', action='store_true')
parser.add_argument('--run', help='Run the created band calculation', action='store_true')
parser.add_argument('--name', metavar='NAME', help='Bandplot directory name', default='band')
# todo path


if __name__ == '__main__':
    args = parser.parse_args()
    ds = [os.path.abspath(d) for d in args.directory] or [os.getcwd()]

    for d in ds:
        os.chdir(d)
        if not os.path.exists("=.in") or not os.path.exists("=.dens"):
            raise RuntimeError('cannot find =.in or =.dens')

        if os.path.exists("out"):
            with open("out", "rb") as fout:
                fout.seek(-80-1, 2)  # 2..from end of file
                assert b"Finished" in fout.readlines()[-1]

        subdir = args.name
        os.mkdir(subdir)
        for fname in glob.glob(d+'/=.*'):
            copy(fname, subdir)

        os.chdir(subdir)
        fed = fedit.Fedit()

        fed.spin(initialspinsplit=False)
        fed.iteration(n=1)
        fed.bandplot(active=True, weights=args.weights, restrictbands=args.weights)
        fed.pipeFedit()

        print('Created', subdir)
        if args.run:
            output = subprocess.check_output(
                ["queue_fplo.py", '.',
                 "--name", "band_" + os.path.basename(d),
                 "--time", str(args.time)])
            print(output)
