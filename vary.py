#!/usr/bin/env python3
import os
import subprocess
from shutil import copy
import glob
import numpy as np
import argparse
import pyfplo.fploio as fploio



parser = argparse.ArgumentParser(description='Create a set of calculations with different parameters, e.g. for relaxation.')
parser.add_argument("param", help='Parameter to vary', choices=['volume'])
parser.add_argument("mode", help='Mode of variation', choices=['factor', 'delta', 'absolute'])
parser.add_argument("value", help='Values to use', type=float, nargs='+')


parser.add_argument('--time', metavar='TIME', help='Requested time in hours', type=float, default=1)
parser.add_argument('--run', help='Queue the created band calculation', action='store_true')


if __name__ == '__main__':
    fplo_parser = fploio.INParser()
    if not os.path.exists("=.in"):
        raise RuntimeError('cannot find =.in')
    try:
        fplo_parser.parseFile("=.in")
    except RuntimeError as e:
        print(e)
    
    
    args = parser.parse_args()
    d = fplo_parser()
    #si = d('structure_information')

    if args.param == 'volume':
        assert args.mode == "factor"  # only really makes sense for factors
        subdir_f = "{}_{}={}"
        lattice_constants = d('lattice_constants').listD
        #fplo_parser.writeFile('test.in')

        for f in args.value:
            d('lattice_constants').listD = (np.cbrt(f) * np.array(lattice_constants)).tolist()
            subdir = subdir_f.format(args.param, args.mode,f)
            os.mkdir(subdir)
            for fname in glob.glob('./=.*'):
                copy(fname, subdir)
            fplo_parser.writeFile(subdir + '/=.in')
            print('Created', subdir)
            
            #queue_fplo
            if args.run:
                output = subprocess.check_output(["queue_fplo.py", subdir, "--name", os.path.basename(subdir), "--time", str(args.time)])
                print(output)

    #os.symlink('.', 'relaxv_fac=1')
