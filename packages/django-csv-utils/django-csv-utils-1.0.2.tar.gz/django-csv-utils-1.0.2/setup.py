#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='django-csv-utils',
    version='1.0.2',
    description='Utilities for working with CSVs in Django',
    long_description=readme,
    author='Ionata Digital',
    author_email='webmaster@ionata.com.au',
    url='https://github.com/ionata/django-csv-utils',
    packages=find_packages('src'),
    install_requires=['django>=1.8.0'],
    package_dir={'': 'src'},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
