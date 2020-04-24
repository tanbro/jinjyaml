#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='jinjyaml',
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    description='A custome YAML tag for Jinja2 template ',
    url='https://github.com/tanbro/jinjyaml',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    python_requires='>=3.5',
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
    install_requires=[
        'jinja2',
        'PyYAML>=5.3,<6.0',
    ],
    extras_require={},

    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
        'write_to': 'src/jinjyaml/version.py',
    },
)
