# -*- coding: utf-8 -*-
"""Module setup file for packaging and installation."""
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()


with open('LICENSE') as f:
    module_license = f.read()

setup(
    name='lmtest',
    version='1.0.0b4',
    description='Lifemapper Testing Library',
    long_description=readme,
    author='CJ Grady',
    author_email='cjgrady@ku.edu',
    url='https://github.com/lifemapper/lm_test',
    license=module_license,
    packages=find_packages(),
    package_dir={
        'example_tests': ['*.json'],
    },
    python_requires='>=3.6, <4',
    entry_points={
        'console_scripts': [
            'run_controller=lmtest.scripts.run_controller:main',
        ],
    },
    install_requires=[
        'psutil'
    ]
)
