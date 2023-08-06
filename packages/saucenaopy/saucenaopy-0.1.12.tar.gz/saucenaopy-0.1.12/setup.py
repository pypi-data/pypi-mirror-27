from setuptools import setup

setup(
  name='saucenaopy',
  version='0.1.12',
  description='Python SauceNAO API wrapper',
  url='https://github.com/ranthai/saucenaopy',
  author='ranthai',
  scripts=['bin/saucenaopy'],
  packages=['saucenaopy'],
  install_requires=['requests']
)
