import sys

from setuptools import setup, find_packages

long_description = open('README.md').read()

if 'upload' in sys.argv:
    import pypandoc

    long_description = pypandoc.convert_text(long_description, 'rst', 'md')

setup(
    name='yu',
    version='0.0.2',
    packages=find_packages(),
    description="pYthon Utilities.",
    long_description=long_description,
)
