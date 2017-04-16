#! /usr/bin/env python

from setuptools import setup, find_packages

setup(
    # http://pythonhosted.org/setuptools/setuptools.html
    name='Role Based Auth System',
    version='0.0.1',
    author='Vidhan Jain',
    author_email='vidhanj1307@gmail.com',

    url='https://github.com/vidhan13j07/Role-Based-Auth-System',
    license='MIT',
    keywords=['rbac', 'authorization'],

    packages=find_packages(),
    scripts=[],
    entry_points={},

    install_requires=[
    ],
    extras_require={
        '_dev': ['wheel', 'nose'],
    },
    include_package_data=True,
    test_suite='nose.collector',

    platforms='any',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)
