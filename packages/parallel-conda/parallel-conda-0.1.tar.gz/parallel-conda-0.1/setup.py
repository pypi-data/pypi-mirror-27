# -*- coding: utf-8 -*-

from setuptools import setup

with open('requirements.txt') as f:
    requires = f.read().strip().split('\n')


setup(
    name='parallel-conda',
    version='0.1',
    description='Drop-in parallel replacement for "conda install ..." procedures.',
    url='https://github.com/milesgranger/parallel-conda',
    maintainer='Miles Granger',
    maintainer_email='miles.r.granger@gmail.com',
    license='MIT',
    install_requires=requires,
    packages=['pconda'],
    entry_points={
        'console_scripts': [
            'pconda = pconda.pconda:pconda'
        ]
    },
    zip_safe=True
)
