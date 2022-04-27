#!/usr/bin/env python3
import os
import argparse
from datetime import timedelta

from slurm import queue_job

#fplo_path = os.environ['HOME'] + "/tmp/FPLO/bin/fplo18.00-52-x86_64"
fplo_path = "/usr/local/fplo/21.00-61/FPLO/bin/fplo21.00-61-x86_64"

parser = argparse.ArgumentParser(description='Queue FPLO run(s).')
parser.add_argument('directory', metavar='DIR', help='FPLO run directory', nargs='+')
parser.add_argument('--name', metavar='NAME', help='Job name', default='FPLO calc')
parser.add_argument('--time', metavar='TIME', help='Requested time in hours', type=float, default=2)

if __name__ == '__main__':
    # todo: command line arguments
    args = parser.parse_args()
    for d in args.directory:
        d = os.path.abspath(d)
        queue_job(
            job_name=args.name,
            data_dir_source=d,
            data_dir=d,
            binpath=fplo_path, 
            time=timedelta(hours=args.time),
            cpus_per_task=2,
            mem_per_cpu=8192)
