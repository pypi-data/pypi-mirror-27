# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def load_file(name):
    with open(name) as fs:
        content = fs.read().strip().strip('\n')
    return content


README = load_file('README.md')

setup(
    name='galaxy-sdk-python3',
    version="0.6",
    author='http://xiangyang.li',
    author_email='wo@xiangyang.li',
    url='http://xiangyang.li/project/galaxy-sdk-python',
    description='Xiaomi Galaxy SDK for Python3',
    long_description=README,
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
    ],
    license='Apache License (2.0)',
)
