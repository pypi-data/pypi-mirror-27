#!/usr/bin/env python
import os
import shutil
from distutils.core import setup

setup(
    name='rst2jira',
    version='0.7.0',
    description='reStructuredText-to-Confluence markup converter',

    author='Kenichiro TANAKA',
    author_email='tanaka.kenichiro@gmail.com',

    maintainer='Roland Puntaier',
    maintainer_email='roland.puntaier@gmail.com',

    url='https://github.com/rpuntaie/rst2jira',

    license='AGPL',
    python_requires='>=3',


    py_modules=['rst2confluence.confluence'],
    scripts=['scripts/rst2jira.py']
)
