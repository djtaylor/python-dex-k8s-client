#!/usr/bin/python
from setuptools import setup, find_packages

# Import the module version
from dex_k8s_client import __version__

with open('requirements-test.txt', 'r') as f:
    tests_require = [x.rstrip() for x in f.readlines()]

with open('requirements.txt', 'r') as f:
    install_requires = [x.rstrip() for x in f.readlines()]

# Run the setup
setup(
    name             = 'dex_k8s_client',
    version          = __version__,
    description      = 'Python bindings for interacting with a Dex server running on Kubernetes.',
    long_description = open('DESCRIPTION.rst').read(),
    author           = 'David Taylor',
    author_email     = 'djtaylor13@gmail.com',
    url              = 'http://github.com/djtaylor/python-dex-k8s-client',
    license          = 'GPLv3',
    install_requires = install_requires,
    test_suite       = 'nose.collector',
    tests_require    = tests_require,
    packages         = find_packages(),
    keywords         = 'grpc rpc api dex k8s kubernetes',
    classifiers      = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Terminals',
    ]
)
