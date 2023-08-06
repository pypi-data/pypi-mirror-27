#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='aiooss',
    version='0.0.1',
    description='A async aliyun OSS library.',
    long_description=readme,
    author='codeif',
    author_email='me@codeif.com',
    url='https://github.com/codeif/aiooss',
    license='MIT',
    install_requires=['aiohttp', 'oss2'],
    packages=find_packages(),
)
