from setuptools import setup
from os import path

f = open('README', 'r')
long_description = f.read()

setup(
    name='xbeetransmission',
    version='0.2.2',
    packages=['xbeetransmission'],
    description='xbeetransmission is a python module is designed to reliably and securely send messages over Xbee modules in out-of-the-box configuration.',
    long_description=long_description,
    url='https://github.com/KyleEvers/xbeetransmission',
    author='Kyle Evers',
    author_email='kyleevers14@yahoo.com',
    license='MIT',
    keywords='xbee'
)
