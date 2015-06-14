# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2'

long_description = (
    read('README.rst')
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    read('AUTHORS')
    + '\n\n' +
    read('CHANGES.rst')
    + '\n\n' +
   'Download\n'
    '========\n')

entry_point = 'bowerrecipe:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = ['zc.buildout', 'mock']

setup(name='bowerrecipe',
      version=version,
      description="zc.buildout recipe to install static resources using Twitter Bower.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Framework :: Buildout :: Recipe',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        ],
      keywords='',
      author='Anshuman Bhaduri',
      author_email='anshuman.bhaduri0@gmail.com',
      url='http://github.com/anshumanb/bowerrecipe',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='bowerrecipe.tests.tests',
      entry_points=entry_points,
      )
