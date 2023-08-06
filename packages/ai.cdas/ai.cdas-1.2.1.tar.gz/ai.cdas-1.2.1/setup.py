import sys
import subprocess
import os
import shutil
# for consistent encoding
from codecs import open
from setuptools import setup, find_packages

version_py = open(
    os.path.join(os.path.dirname(__file__), 'version.py')
).read().strip().split('=')[-1].replace('"', '')

# Get the long description from the README file
with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst'),
    encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ai.cdas',
    version='{ver}'.format(ver=version_py),
    description='Python interface to CDAS data via REST API',
    long_description=long_description,
    url='https://bitbucket.org/isavnin/ai.cdas',
    author='Alexey Isavnin',
    author_email='alexey.isavnin@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='coordinated data analysis web cdaweb cdas spdf research space physics data facility nasa science',
    packages=find_packages('src', exclude=['test*']),
    package_dir={'': 'src'},
    install_requires = ['numpy', 'requests', 'wget', 'astropy'],
    extras_require = {
        'CDF': ['spacepy']
    }
)
