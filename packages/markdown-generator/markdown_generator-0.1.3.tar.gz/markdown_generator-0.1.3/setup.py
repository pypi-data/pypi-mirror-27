# -*- coding: utf-8 -*-

from distutils.core import setup
import os


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

MAJOR = 0
MINOR = 1
# BUILD = os.environ.get('TRAVIS_BUILD_NUMBER', 'dev')
BUILD = 3

setup(
    name='markdown_generator',
    version='{}.{}.{}'.format(MAJOR, MINOR, BUILD),
    description='Python package for generating GitHub-flavored markdown',
    long_description=readme,
    author='Corey McCandless',
    author_email='crm1994@gmail.com',
    url='https://github.com/cmccandless/markdown-generator',
    license=license,
    packages=['markdown_generator']
#    packages=find_packages(exclude=('tests', 'docs'))
)
