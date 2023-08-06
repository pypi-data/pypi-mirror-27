# -*- coding: utf-8 -*-
"""
    cubeswriter
    ~~~~~~~~~~~

    cubeswriter is a tool for creating write-layer SQLalchemy models
"""

from setuptools import setup, find_packages


def get_long_description():
    with open('README.md') as f:
        result = f.read()
    return result


setup(
    name='cubeswriter',
    version='0.0.1',
    license='MIT',
    author='Michael Pérez',
    author_email='mpuhrez@gmail.com',
    description='Cubeswriter is a tool for creating write-layer SQLalchemy models from Cubes model JSON',
    url="https://github.com/puhrez/CubesWriter.git",
    keywords=['cubes', 'sql', 'write-layer', 'data'],
    packages=find_packages(),
    include_package_data=True,
    platforms='any'
)
