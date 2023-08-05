# -*- coding: utf-8 -*-
from setuptools import setup

requires = [
    'requests==2.18.4',
]

extras_require = {
    'test': [
        'pytest==3.3.0',
    ],
}

setup(name='smart-fflags-client',
      version='0.0.1',
      description='Smart Dashboard to manage feature flags Client',
      author='Daniel Debonzi',
      author_email='debonzi@gmail.com',
      install_requires=requires,
      extras_require=extras_require,
      url='https://bitbucket.org/debonzi/smartflag-client',
      packages=['smartflags'],
      )
