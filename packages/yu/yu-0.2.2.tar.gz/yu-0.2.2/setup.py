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
    url='https://github.com/huyx/yu',
    description="pYthon Utilities.",
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ]
)
