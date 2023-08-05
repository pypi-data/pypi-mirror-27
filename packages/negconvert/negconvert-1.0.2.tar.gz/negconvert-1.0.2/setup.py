# -*- coding: utf-8 -*-
 
 
"""setup.py: setuptools control."""
 
 
from setuptools import setup
 
setup(
    name = 'negconvert',
    packages = ['negconvert'],
    entry_points = {
        "console_scripts": ['negconvert = negconvert.negconvert:main']
        },
    version='1.0.2',
    description = 'A command line application to normalize text from people tweets for further data processing and visualization.',
    author='dylan salopek,quan nguyen',
    author_email='dylan.salopek@ttu.edu,quan.nguyen@ttu.edu',
    url='https://github.com/litpuvn/flu-shot',
    package_data={
        'negconvert': ['contractions.csv',
                 'opposites.csv',
                 'synonyms.csv']
    },
    install_requires=['pyenchant', 'stanfordcorenlp'],
    python_requires='>=3',
    )