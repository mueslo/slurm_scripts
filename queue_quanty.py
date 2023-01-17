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
parser.add_argument('--ncpus', metavar='NCPUS', help='requested # cpus', type=int, default=4)
parser.add_argument('--mempercpu', metavar='MEM', help='requested mem per cpu in MB', type=int, default=2048)

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
            env={'OMP_NUM_THREADS': args.ncpus},
            binpath=quanty_path,
            arguments=os.path.basename(p),
            time=timedelta(hours=args.time),
            cpus_per_task=args.ncpus,
            mem_per_cpu=args.mempercpu,
            verbosity=1)

