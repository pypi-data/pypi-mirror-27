'''
Created on Dec 8, 2017

@author: maltaweel
'''
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='webbyApp',
      version='0.1',
      description='The funniest joke in the world',
      url='https://github.com/maltaweel/webbyApp.git',
      author='Mark Altaweel',
      author_email='markaltaweel@example.com',
      install_requires=['beautifulsoup4'],
      python_requires='>=2.7',
      license='MIT',
      packages=['src'],
      zip_safe=False)
