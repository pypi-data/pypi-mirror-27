# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 17:13:44 2017

@author: SKT
"""

from setuptools import setup, find_packages

setup(name='skt7',
      version='0.1',
      description='Library for api of all my python codes',
      url='https://github.com/skt7/python-skt',
      author='SKT',
      author_email='developerskt@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests'])