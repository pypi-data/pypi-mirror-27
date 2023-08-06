#!/usr/bin/python
# 3.5
"""
pypinner.cli

Ensure requirements.txt files reflect versions in pip freeze.
Finds requirements*.txt files recursively and fixes them.

Usage:
  pypinner
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
    return glob.glob("./**/requirements*.txt", recursive=True)


def pip_freeze():
    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)
    frozen = dict([dep.decode().split('==') for dep in result.stdout.splitlines() if '==' in dep.decode()])
    return frozen


def run(arguments):
    files = find_files()
    frozen = pip_freeze()
    with fileinput.input(files=files, inplace=True, backup=".bak") as requirements:
        for req in requirements:
            req = req.strip()
            if req in frozen:
                req = "{}=={}".format(req, frozen[req])
                sys.stderr.write("Pinning: {}\t{}\n".format(fileinput.filename(), req))
            else:
                sys.stderr.write("Leaving: {}\t{}\n".format(fileinput.filename(), req))
            print(req)


def main():
    arguments = docopt(__doc__, version=pypinner.__version__)
    run(arguments)
