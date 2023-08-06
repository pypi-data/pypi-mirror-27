import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

"""
    Setup.py
    Required files:
        README.md
        {PROJECT}/version.txt
        MANIFEST.in
        requirements.txt
        requirements_test.txt
"""

# Mandatory project/module name
PROJECT = 'pypinner'
KEYWORDS = "python pip freeze version pinner"
URL = ""
# Optional entrypoint {PROJECT}.cli:main()
CLI = 'pypinner'


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            '-s',
            '-ra',
            '--verbose',
            '--flake8',
            '--isort',
            '--cov-report=xml',
            '--cov-report=term-missing',
            '--cov={}'.format(PROJECT),
            '--junitxml=junit.xml',
        ]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def slurp(file):
    return open(os.path.join(os.path.abspath(os.path.dirname(__file__)), file)).read().strip()


REQUIREMENTS = slurp('requirements.txt').splitlines()
REQUIREMENTS_TEST = ['setuptools']
REQUIREMENTS_TEST.extend(slurp('requirements_test.txt').splitlines())
REQUIREMENTS_TEST.extend(REQUIREMENTS)

setup_cfg = {
    'name': PROJECT,
    'version': slurp(os.path.join(PROJECT, "version.txt")),
    'license': "MIT",
    'description': slurp('README.md').splitlines()[3],
    'long_description': slurp('README.md'),
    'url': URL,
    'keywords': KEYWORDS,
    'packages': find_packages(),
    'py_modules': [PROJECT],
    'cmdclass': {'test': PyTest},
    'tests_require': REQUIREMENTS_TEST,
    'install_requires': REQUIREMENTS,
    'dependency_links': [],
    'package_data': {
        '': ['*.txt', '*.md', '*.json'],
    },
    'classifiers': [
        # Development Status: 3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
}

if CLI:
    setup_cfg['entry_points'] = {
        'console_scripts': [
            '{} = {}.cli:main'.format(CLI, PROJECT)
        ]
    }

setup(**setup_cfg)
