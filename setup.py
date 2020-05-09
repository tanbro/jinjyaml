#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import linesep

from setuptools import find_packages, setup

setup(
    name='jinjyaml',
    description='Application specific YAML tag of Jinja2 template',
    url='https://github.com/tanbro/jinjyaml',
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',

    long_description=('{0}---{0}'.format(linesep * 2)).join(
        open(file, encoding='utf-8').read().strip()
        for file in ('README.md', 'CHANGELOG.md', 'AUTHORS.md')
    ),
    long_description_content_type='text/markdown',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    python_requires='>=3.5',
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
    install_requires=[
        line for line in map(lambda s: s.strip(), open('requirements.txt', encoding='utf-8'))
        if line and not line.startswith('#')
    ],

    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
        'write_to': 'src/jinjyaml/version.py',
    },
)
