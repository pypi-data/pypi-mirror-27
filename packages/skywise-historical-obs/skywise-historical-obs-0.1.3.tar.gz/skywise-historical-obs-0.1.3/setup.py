#!/usr/bin/env python
from setuptools import setup

setup(
    name='skywise-historical-obs',
    version='0.1.3',
    package_data={'': ['README.md']},
    packages=['skywisehistoricalobs'],
    install_requires=[
        'skywise-rest-client',
        'voluptuous'
    ],

    # metadata for upload to PyPI
    author='Weather Decision Technologies',
    author_email='support@wdtinc.com',
    description='SkyWise Historical Obs Python Client Library',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    )
)
