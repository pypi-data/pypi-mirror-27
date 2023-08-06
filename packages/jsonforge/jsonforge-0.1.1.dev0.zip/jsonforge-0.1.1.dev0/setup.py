#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
        'archieml',
        'attrdict',
        'boto3',
        'botocore',
        'certifi',
        'chardet',
        'dataset',
        'dateparser',
        'docutils',
        'fire',
        'idna',
        'jmespath',
        'lxml',
        'pandas',
        'pyquery',
        'python-dateutil',
        'requests',
        'ruamel.yaml',
        's3transfer',
        'simplejson',
        'six',
        'unicode-slugify',
        'urllib3',
        'xmljson'
]

setup_requirements = [
    # TODO(mvtango): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='jsonforge',
    version='0.1.1dev',
    description="""Make nice JSON files out of ugly (X|HT)ML, CSV or JSON blobs found on the Internet using JMESPath, CSS and XPath""",
    long_description=readme + '\n\n' + history,
    author="Martin Virtel",
    author_email='mv@datenfreunde.com',
    url='https://bitbucket.com/datenfreunde/jsonforge',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    python_requires='>=3.6',
    keywords='Text, JSON, CSV, JMESPath, CSS, XPath',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    entry_points={
        'console_scripts': [
            'jsonforge = jsonforge.cmdline:run'
        ]
    }
)
