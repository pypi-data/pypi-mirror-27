#!/usr/bin/env python3

from setuptools import setup

setup(name='tap-lol',
      version='0.0.1.dev2',
      description='Singer.io tap for extracting data from the League of Legends API',
      author='scirner22',
      url='https://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      install_requires=[
          'singer-python==5.0.2',
          'requests==2.12.4',
          'pendulum==1.2.0',
          'backoff==1.4.3',
      ],
      entry_points='''
          [console_scripts]
          tap-lol=tap_lol.tap_lol:main
      ''',
      packages=['tap_lol'],
      package_data = {
          'tap_lol/schemas': [
              'matches.json',
          ],
    },
    include_package_data=True,
)
