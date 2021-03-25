# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

#with open('README.md') as f:
#    readme = f.read()
readme = 'LM Test readme.'


with open('LICENSE') as f:
    license = f.read()

setup(
    name='Lifemapper Testing Library',
    version='0.1.0',
    description='Lifemapper Testing Library',
    long_description=readme,
    author='CJ Grady',
    author_email='cjgrady@ku.edu',
    url='https://github.com/lifemapper/lm_test',
    license=license
    #packages=find_packages(exclude=('tests', 'docs')),
    #install_requires=[
    #    'requests']
)
