from setuptools import setup
from inspect import cleandoc


_version = {}
execfile('hoursofoperation/_version.py', _version)


setup(
  name = 'hoursofoperation',
  packages = ['hoursofoperation', 'hoursofoperation.test'],
  version = _version['__version__'],
  description = 'Utilities for loading and doing calculations with a partner\'s hours of operations configration.',
  author = 'Ashley Fisher',
  author_email = 'fish.ash@gmail.com',
  url = 'https://github.com/Brightmd/hoursofoperation',
  keywords = ['hours'],
  classifiers = [],
  scripts = [],
  install_requires=cleandoc('''
    codado>=0.4.997,<0.6
    python-dateutil==2.4.0
    pytz==2015.4
    ''').split()
)
