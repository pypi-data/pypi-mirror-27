#!/usr/bin/python
# 3.5
"""
pinner.cli

Command line program for pinner

Usage:
  pinner <project_dir>
  pinner (-h | --help)
  pinner --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from docopt import docopt
import glob
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(relativeCreated)6d %(threadName)s %(message)s'
)
LOG = logging.getLogger()

def main():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'version.txt')) as f:
        VERSION = f.read().strip()

    arguments = docopt(__doc__, version=VERSION)

    g=glob.glob("./**/requirements*.txt",recursive=True)
    print(g)
