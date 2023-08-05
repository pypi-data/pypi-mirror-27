#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

setup(
    name='wickedql',
    version='0.0.1',
    description="Wicked Cool GraphQL Library for Python",
    long_description=readme,
    author="WickedQL",
    author_email='admin@penny-api.com',
    url='https://github.com/wickedql/wickedql',
    py_modules=['wickedql'],
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='wickedql',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
