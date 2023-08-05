#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = [
    'tebless',
    'reportlab',
    'requests',
    'tqdm',
    'fire'
]

SETUP_REQUIREMENTS = [
    'pytest-runner',
]

TEST_REQUIREMENTS = [
    'pytest',
]

setup(
    name='vimanga',
    version='0.2.1',
    description="App for download manga",
    long_description=README + '\n\n' + HISTORY,
    author="Michel Betancourt",
    author_email='MichelBetancourt23@gmail.com',
    url='https://github.com/akhail/vimanga',
    packages=find_packages(include=['vimanga', 'vimanga.*']),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'vimanga = vimanga.__main__:main'
        ]
    },
    license="MIT license",
    zip_safe=False,
    keywords='vimanga',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,
)
