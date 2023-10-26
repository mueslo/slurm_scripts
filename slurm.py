# make a slurm job file

import os
import subprocess
from datetime import timedelta
from string import Template
from tempfile import NamedTemporaryFile, mkdtemp

jobs_dir = os.path.join(os.environ['HOME'], 'jobs')
share_dir = os.path.join(os.environ['HOME'], 'share')
job_dir = os.path.join(jobs_dir, '$SLURM_JOB_ID')
out_path = os.path.join(jobs_dir, '$SLURM_JOB_ID.out')
data_dir_default = os.path.join(job_dir, 'data')

template_path = os.path.join(share_dir, "slurm_job.sh.template")
template = Template(open(template_path, 'r').read())


def make_job_file(verbosity=2, **kwargs):
    #mangle kwargs
    assert os.path.exists(kwargs['data_dir_source'])
    assert os.path.exists(kwargs['binpath'])

    if 'binname' not in kwargs:
        assert os.path.isfile(kwargs['binpath'])
        kwargs['binname'] = os.path.basename(kwargs['binpath'])

    kwargs.setdefault('arguments', '')

    kwargs.setdefault('time', timedelta(hours=2))
    kwargs.setdefault('ntasks', 1)
    kwargs.setdefault('cpus_per_task', 1)
    kwargs.setdefault('mem_per_cpu', 512)
    kwargs.setdefault('job_name', 'Unnamed job')

    kwargs.setdefault('job_dir', job_dir)
    kwargs.setdefault('out_path', out_path)
    kwargs['out_path_sbatch'] = out_path.replace("$SLURM_JOB_ID", "%j")

    kwargs['data_dir_default'] = data_dir_default
    kwargs.setdefault('data_dir', data_dir_default)

    kwargs.setdefault('env', dict())
    kwargs['env'] = "\n".join(
        f"export {k}={v}" for k, v in kwargs['env'].items())

    kwargs.setdefault('w2k_princess', '')

    if 'partition' not in kwargs:
        t = kwargs['time']
        p = None
        if t <= timedelta(hours=2):
            p = 'short'
        elif t <= timedelta(days=2):
            p = 'medium'
        elif t <= timedelta(days=14):
            p = 'long'
        elif t <= timedelta(days=28):
            p = 'extra_long'
        kwargs['partition'] = p

    jobfile = NamedTemporaryFile(
        mode='w', prefix='slurmjob_', suffix=".sh", delete=False)

    minutes, seconds = divmod(kwargs['time'].seconds, 60)
    hours, minutes = divmod(minutes, 60)
    kwargs['time'] = f"{kwargs['time'].days}-{hours:02}:{minutes:02}:{seconds:02}"

    filled = template.substitute(**kwargs)
    jobfile.write(filled)
    if verbosity >= 2:
        print(filled)
    return jobfile.name


def run_command(*command, verbosity=2):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output and verbosity >= 1:
            print(output.strip().decode("utf8"))
    rc = process.poll()
    return rc


def queue_job(verbosity=2, **kwargs):
    job_file = make_job_file(**kwargs, verbosity=verbosity)
    print('Temporary job file: {}'.format(job_file))
    rc = run_command("sbatch", job_file, verbosity=verbosity)


if __name__ == '__main__':
    print('testing...')
    tmpdir = os.path.join(os.environ['HOME'], 'tmp/slurm_test')
    #print(make_job_file(jobdir=tmpdir, binpath='/usr/bin/true', partition='debug', time=timedelta(seconds=1)))
    queue_job(data_dir_source=tmpdir, data_dir=os.path.join(tmpdir, 'finished'), binpath='/usr/bin/true', partition='debug', time=timedelta(seconds=10))
