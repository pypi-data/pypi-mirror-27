from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rp',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='0.0.993',
    description='A sample Python project',
    url='https://github.com/RyannDaGreat/Quick-Python',
    author='Ryan Burgert',
    author_email='ryancentralorg@gmail.com',
    license='MIT',
    keywords='not_searchable_yet',
    packages=["rp",'rp.rp_ptpython'],
    install_requires=["ptpython","numpy"],
    # scripts=['rpie.py']
)