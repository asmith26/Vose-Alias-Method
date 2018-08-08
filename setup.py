import os
import sys
import unittest
from setuptools import setup


_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()


def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test*.py')
    return test_suite


setup(
    name='Vose-Alias-Method',
    version='1.0.0',
    description=('Python implementation of Vose\'s alias method, an efficient algorithm for sampling from a discrete probability distribution.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='asmith26',
    url='https://github.com/asmith26/Vose-Alias-Method.git',
    license='Apache-2.0',
    packages=['vose_sampler'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={
        'console_scripts': ['vose-sampler=vose_sampler.vose_sampler:main'],
    },
    test_suite='setup.test_suite',
)
