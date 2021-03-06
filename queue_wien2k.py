#!/usr/bin/env python2
import os
import argparse
from datetime import timedelta

from slurm import queue_job

wien2k_path = os.environ['HOME'] + "/tmp/wien2k_19.1"

parser = argparse.ArgumentParser(description='Queue Wien2K run.')
parser.add_argument('directory', metavar='DIR', help='Wien2K run directory')
parser.add_argument('--name', metavar='NAME', help='Job name', default='Wien2K calc')
parser.add_argument('--time', metavar='TIME', help='Requested time in hours', type=float, default=48)
parser.add_argument('--args', metavar='ARGS', help='run_lapw arguments', type=str, default="-p")
parser.add_argument('--debug', action='store_true', help='use debug pool')

if __name__ == '__main__':
    # todo: command line arguments
    args = parser.parse_args()
    d = os.path.abspath(args.directory)
    assert os.path.isdir(d)

    requested_time = timedelta(hours=args.time)
    kwargs = {}
    if args.debug:
        kwargs['partition'] = 'debug'
        requested_time = timedelta(minutes=5)

    queue_job(
        job_name=args.name,
        data_dir_source=d,
        data_dir=d,
        w2k_princess=os.path.basename(d),
	arguments=args.args,
        binpath=wien2k_path,
	binname="wien2k_19.1/run_lapw",
        time=requested_time,
	debug=args.debug,
        cpus_per_task=6,
        mem_per_cpu=1024,
        **kwargs)
