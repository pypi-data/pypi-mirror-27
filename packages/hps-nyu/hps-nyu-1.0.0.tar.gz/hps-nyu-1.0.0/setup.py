"""
Setup script for the library
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hps-nyu',
    version='1.0.0',
    description='Tools for architecture for HPS games',
    long_description=long_description,
    url='https://gitlab.com/mmc691/hps-project',
    author='Team Rocket',
    author_email='mmc691@nyu.edu',
    download_url='https://gitlab.com/mmc691/hps-project/',
    platforms=['Linux', 'MacOS', 'Windows'],
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['pyzmq'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: C++',
        'Programming Language :: Java',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Games/Entertainment :: Turn Based Strategy',
        'Topic :: Utilities'
        ]
)
