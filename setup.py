#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='jinjyaml',
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    description='A custom YAML tag for Jinja2 template ',
    url='https://github.com/tanbro/jinjyaml',

    long_description=('\n' * 2).join(
        open(file, encoding='utf-8').read()
        for file in ('README.md', 'CHANGELOG.md', 'AUTHORS.md')
    ),
    long_description_content_type='text/markdown',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    python_requires='>=3.5',
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
    install_requires=[
        line.strip()
        for line in open('requirements.txt', encoding='utf-8')
        if line.strip() and not line.strip().startswith('#')
    ],

    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
        'write_to': 'src/jinjyaml/version.py',
    },
)
