# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='getdoi',
    version='0.1.1',
    description='Get journal\'s DOI from article citation text.',
    long_description=readme,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: MacOS X",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    author='Yuto Mizutani',
    author_email='yuto.mizutani.dev@gmail.com',
    install_requires=['beautifulsoup4', 'articleinfo'],
    url='https://github.com/YutoMizutani/getdoi',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests',
    scripts=['scripts/getdoi']
)
