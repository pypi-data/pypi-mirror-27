#  -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='confobj',
    version='1.2.0',
    description='Object overridable by external configuration',
    url='https://github.com/datasets-org/confobj',
    author='Vit Listik',
    author_email='tivvit@seznam.cz',
    license='MIT',
    install_requires=[
       "typing",
       "pyYAML",
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords="conf yaml json env",
    packages=["confobj"],
)