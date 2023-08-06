#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='lawrenceliu',
    version='0.0.1',
    author='lawrence',
    author_email='liuchu1.0@gmail.com',
    url='https://github.com/LawrenceLiu',
    description=u'lawrenceliu的pypi测试',
    packages=['lawrenceliu'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'lawrence=lawrenceliu:go',
            'contact=lawrenceliu:contact'
        ]
    }
)