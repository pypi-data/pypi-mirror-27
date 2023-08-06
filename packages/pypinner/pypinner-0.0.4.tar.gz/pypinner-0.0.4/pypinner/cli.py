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
        Naive split on == in requirements file.
        Also, only really interested in hard pinned requirements.
    """
    return dict([dep.split('==') for dep in req.splitlines() if '==' in dep])


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
        for req in requirements:
            req = req.strip()
            if req in frozen:
                req = "{}=={}".format(req, frozen[req])
                sys.stderr.write("Pinning: {}\t{}\n".format(fileinput.filename(), req))
            else:
                sys.stderr.write("Leaving: {}\t{}\n".format(fileinput.filename(), req))
            print(req)
    return 0


def main():
    """
        Main entrypoint.
    """
    arguments = docopt(__doc__, version=pypinner.__version__)
    exit(run(arguments))
