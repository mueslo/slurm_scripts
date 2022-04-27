#!/usr/bin/env python3
import os
import argparse
from shutil import copy
import glob
import numpy as np
import pyfplo.fedit as fedit
import subprocess

parser = argparse.ArgumentParser(description='Create and queue bandplot calculation.')
parser.add_argument('directory', metavar='DIR', help='FPLO run directory', nargs='*')
parser.add_argument('--time', metavar='TIME', help='Requested time in hours', type=float, default=1)
parser.add_argument('--weights', help='Get bandweights', action='store_true')

if __name__ == '__main__':
	args = parser.parse_args()
	ds = [os.path.abspath(d) for d in args.directory] or [os.getcwd()]
	
	for d in ds:
		os.chdir(d)
		if not os.path.exists("=.in") or not os.path.exists("=.dens"):
			raise RuntimeError('cannot find =.in or =.dens')

		subdir='band'
		os.mkdir(subdir)
		for fname in glob.glob(d+'/=.*'):
			copy(fname, subdir)

		os.chdir(subdir)
		fed = fedit.Fedit()

		fed.bandplot(active=True, weights=args.weights)
		fed.pipeFedit()

		print('Created', subdir)
		output = subprocess.check_output(["queue_fplo.py", '.', "--name", "band_"+os.path.basename(d), "--time", str(args.time)])
		print(output)
