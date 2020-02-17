# -*- coding: utf-8 -*-

import os
from codecs import open

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Dependencies.
with open('requirements.txt') as f:
    requirements = f.readlines()
install_requires = [t.strip() for t in requirements]

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mtnhubsnow',
    version='0.1',
    description='Simplified and standardized access to MountainHub API snow depth data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/communitysnowobs/mountainhub-api',
    author='',
    author_email='',
    maintainer='Emilio Mayorga',
    maintainer_email='emiliom@uw.edu',
    python_requires='>=3',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering'
    ],
    keywords=[],
    packages=find_packages(),
    install_requires=install_requires,
)