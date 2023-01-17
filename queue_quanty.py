#!/usr/bin/env python3
import os
import argparse
from datetime import timedelta

from slurm import queue_job

quanty_path = os.environ['HOME'] + "/bin/Quanty"

parser = argparse.ArgumentParser(description='Queue Quanty calc(s).')
parser.add_argument('path', metavar='DIR', help='Quanty lua script', nargs='+')
parser.add_argument('--name', metavar='NAME', help='Job name', default='Quanty calc')
parser.add_argument('--time', metavar='TIME', help='Requested time in hours', type=float, default=2)

if __name__ == '__main__':
    # todo: command line arguments
    args = parser.parse_args()
    for p in args.path:
        p = os.path.abspath(p)
        assert os.path.isfile(p)
        queue_job(
            job_name=args.name,
            data_dir_source=p,
            data_dir=p+'_out',
            binpath=quanty_path,
            arguments=os.path.basename(p),
            time=timedelta(hours=args.time),
            cpus_per_task=2,
            mem_per_cpu=8192,
            verbosity=1)

