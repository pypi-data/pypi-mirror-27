#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'keras >= 2.0',
    'tensorflow >= 1.4'
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='linked_neurons',
    version='0.1.0',
    description="Keras implementation of the article \"Solving internal covariate shift in deep learning with linked neurons\"",
    long_description=readme + '\n\n' + history,
    author="Carles R. Riera Molina",
    author_email='carlesrieramolina@gmail.com',
    url='https://github.com/blauigris/linked_neurons',
    packages=find_packages(include=['linked_neurons']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='linked_neurons deep-learning machine-learning neural-networks',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
'Topic :: Scientific/Engineering :: Artificial Intelligence',


        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
