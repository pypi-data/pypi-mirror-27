# -*- coding:utf-8 -*-
"""Package install script
"""

from os import path
from setuptools import setup, find_packages

BASE_PATH = path.abspath(path.dirname(__file__))
with open(path.join(BASE_PATH, 'README.rst'), encoding='utf-8') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name='zhao',
    version='0.0.10',
    description='A sweet Python cake for all Pythoners!',
    long_description=LONG_DESCRIPTION,
    url='http://nixoahz.com',
    license='GNU General Public License v3 (GPLv3)',
    author='Zhao Xin',
    author_email='7176466@qq.com',
    platforms='cross-platform',
    python_requires='>=3.6',
    install_requires=[
        'mysqlclient>=1.3.12',
        'requests>=2.18.4'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='Python Implementation',
    packages=find_packages(exclude=[])
)
