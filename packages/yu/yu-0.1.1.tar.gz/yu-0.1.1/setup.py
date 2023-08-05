import sys

from setuptools import setup, find_packages
from yu import version

long_description = open('README.md', encoding='utf-8').read()

if 'upload' in sys.argv:
    import pypandoc

    long_description = pypandoc.convert_text(long_description, 'rst', 'md')

setup(
    name='yu',
    version=version,
    packages=find_packages(exclude=['tests']),
    description="pYthon Utilities.",
    long_description=long_description,
)
