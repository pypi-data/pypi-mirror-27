# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='parallel-conda',
    version='0.2.3',
    description='Drop-in parallel replacement for "conda install ..." procedures.',
    url='https://github.com/milesgranger/parallel-conda',
    maintainer='Miles Granger',
    maintainer_email='miles.r.granger@gmail.com',
    license='MIT',
    install_requires=['click>=6.6', 'futures'],
    packages=['pconda'],
    entry_points={
        'console_scripts': [
            'pconda = pconda.pconda:pconda'
        ]
    },
    zip_safe=True
)
