#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Twisted==16.1.1',
    'zope.interface==4.1.3',
]

test_requirements = [
    'coverage',
    'flake8',
    'mock',
    'tox',
]

setup(
    name='ethproxy',
    version='1.0.2',
    description="Ethereum stratum proxy",
    long_description=readme,
    author="Jon Robison",
    author_email='narfman0@gmail.com',
    url='https://github.com/narfman0/eth-proxy',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="GPL2 license",
    zip_safe=True,
    keywords='crypto eth ethereum proxy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': ['ethproxy=ethproxy.cli:main'],
    }
)
