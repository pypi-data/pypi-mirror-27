#!/usr/bin/env python3

from setuptools import setup

setup(name='tio',
    version='3.0',
    description='Helper libraries and utils for Twinleaf I/O (TIO) devices',
    url='https://code.twinleaf.com/open-source/tio-python',
    author='Thomas Kornack',
    author_email='kornack@twinleaf.com',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        "PyYAML",
        "pyserial",
        "blessings",
    ],
    packages=[
        'tio',
        'slip',
        'tldevice',
    ],
    scripts=[
        'examples/itio.py'
    ],
    zip_safe=False)
