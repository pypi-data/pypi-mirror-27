PyPinner
========

Ensure requirements.txt files reflect versions in pip freeze.

Command Line Usage
------------------

```
Ensure requirements.txt files reflect versions in pip freeze.
Finds requirements*.txt files recursively and fixes them.

Usage:
  pypinner
  pypinner (-h | --help)
  pypinner --version

Options:
  -h --help     Show this screen.
  --version     Show version.

```

Example
-------

```
$pypinner
Leaving: ./requirements_test.txt  flake8==3.5.0
Leaving: ./requirements_test.txt  pytest==3.3.1
Leaving: ./requirements_test.txt  pytest-flake8==0.9.1
Leaving: ./requirements_test.txt  pytest-isort==0.1.0
Leaving: ./requirements_test.txt  pytest-bdd==2.19.0
Leaving: ./requirements_test.txt  flake8-isort==2.2.2
Leaving: ./requirements_test.txt  pytest-cov==2.5.1
Leaving: ./requirements_test.txt 
Pinning: ./requirements.txt docopt==0.6.2

```

Installation
------------

* python setup.py install

* pip install pinner
