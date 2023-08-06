#!/usr/bin/python
# 3.5
"""
pypinner.cli

Ensure requirements.txt files reflect versions in pip freeze.
Finds requirements*.txt files recursively and fixes them.

Usage:
  pypinner
  pypinner -f <frozen_requirements.txt>
  pypinner (-h | --help)
  pypinner --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

import fileinput
import glob
import logging
import re
import subprocess
import sys

import pypinner
from docopt import docopt

logging.basicConfig(
    level=logging.INFO,
    format='%(relativeCreated)6d %(threadName)s %(message)s'
)
LOG = logging.getLogger()


def find_files():
    """
        Find requirements files recursively from PWD.
        Searches for requirements*.txt
    """
    return glob.glob("./**/requirements*.txt", recursive=True)


def req_to_dict(req):
    """
        Naive split on *= in requirements file.
        Also, only really interested in hard pinned requirements.
    """
    reqs = {}
    for dep in req.splitlines():
        parts = re.split(r'[<>~=]=', dep)
        if len(parts) == 2:
            (package, version) = parts
            reqs[package.lower()] = (package, version)
    return reqs


def get_pip_freeze():
    """
        Run pip freeze and return requirements as a dict.
    """
    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)
    req = result.stdout.decode()
    return req_to_dict(req)


def get_frozen_requirements(file):
    """
        Load requirements from a file and return as a dict.
    """
    with open(file, "r") as f:
        return req_to_dict(f.read())


def run(arguments):
    """
        Run the pypinner with the supplied arguments.
    """
    files = find_files()
    if arguments['-f']:
        frozen = get_frozen_requirements(arguments['<frozen_requirements.txt>'])
    else:
        frozen = get_pip_freeze()
    with fileinput.input(files=files, inplace=True, backup=".bak") as requirements:
        for dep in requirements:
            package = re.split(r'[<>~=]=', dep.strip())[0].strip()
            if not package or len(package) == 0 or package.startswith('#'):
                print(dep)
                continue
            if package.lower() in frozen:
                dep = "{}=={}".format(*frozen[package.lower()])
                sys.stderr.write("Pinning: {}\t{}\n".format(fileinput.filename(), dep))
            else:
                sys.stderr.write("Leaving: {}\t{}\n".format(fileinput.filename(), dep))
            print(dep)
    return 0


def main():
    """
        Main entrypoint.
    """
    arguments = docopt(__doc__, version=pypinner.__version__)
    exit(run(arguments))
