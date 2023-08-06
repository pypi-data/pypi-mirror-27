"""
author: created by zhao.guangyao on 11/30/17.
desc: 
"""
from setuptools import setup, find_packages

setup(
    name='finogeeks',
    version='0.1.4',
    description='Private purpose package for finogeeks',
    packages=find_packages(include=['finogeeks']),
    install_requires=['pymongo', 'kafka'],
)
