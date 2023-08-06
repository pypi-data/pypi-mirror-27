import os
import re
import sys
from setuptools import setup, find_packages
from urllib.parse import urlparse

PACKAGE_NAME = 'd3m_metadata'
MINIMUM_PYTHON_VERSION = 3, 6
REQUIREMENTS_MAP = {}


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {}.{}+ is required.".format(*MINIMUM_PYTHON_VERSION))


def read_package_variable(key):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, '__init__.py')
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ')
            if parts and parts[0] == key:
                return parts[-1].strip("'")
    assert False, "'{0}' not found in '{1}'".format(key, module_path)


def package_from_requirement(requirement):
    """Convert pip requirement string to a package name."""
    if requirement.startswith('git+'):
        requirement_path = urlparse(requirement).path
        cleaned_repository_name = re.sub(r'-', r'_', re.sub(r'\.git(@.+)?$', r'', requirement_path.split('/')[-1]))
        if cleaned_repository_name in REQUIREMENTS_MAP:
            return REQUIREMENTS_MAP[cleaned_repository_name]
        else:
            return cleaned_repository_name
    else:
        return re.sub(r'\[[^\]]*\]', '', requirement)


def read_requirements():
    """Read the requirements."""
    with open('requirements.txt') as requirements:
        return [package_from_requirement(requirement.strip()) for requirement in requirements]


check_python_version()

setup(
    name=PACKAGE_NAME,
    version=read_package_variable('__version__'),
    description='Metadata for values and primitives',
    author='DARPA D3M Program',
    packages=find_packages(exclude=['contrib', 'docs', 'site', 'tests*']),
    package_data={'d3m_metadata': ['schemas/*/*.json']},
    install_requires=read_requirements(),
    url='https://gitlab.com/datadrivendiscovery/metadata',
)
