#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

install_requirements = [
    "future",
    "pandas==0.21.1",
    "numpy",
    "scipy",
    "joblib",
    "python-crfsuite==0.9.5",
    "scikit-learn",
    "xgboost"
]

setup_requirements = [
    "pandas==0.21.1",
    "numpy",
    "joblib"
]

test_requirements = [
    # TODO: put package test requirements here
    "tox",
    "pandas==0.21.1",
    "numpy",
    "joblib"
]

setup(
    name='languageflow',
    version='1.1.6-rc',
    description="Useful stuffs for NLP experiments",
    long_description=readme + '\n\n' + history,
    author="Vu Anh",
    author_email='brother.rain.1024@gmail.com',
    url='https://github.com/undertheseanlp/languageflow',
    packages=find_packages(include=['languageflow']),
    include_package_data=True,
    install_requires=install_requirements,
    license="MIT license",
    zip_safe=False,
    keywords='languageflow',
    entry_points={
        'console_scripts': [
            'languageflow=languageflow.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
