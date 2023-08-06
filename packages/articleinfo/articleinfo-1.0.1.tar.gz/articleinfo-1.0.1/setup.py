# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
with open('README.md') as f:
    readme = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='articleinfo',
    version='1.0.1',
    description='Get article information from your entered citation text.',
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
    install_requires=[],
    url='https://github.com/YutoMizutani/articleinfo',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests',
    scripts=['scripts/articleinfo']
)
