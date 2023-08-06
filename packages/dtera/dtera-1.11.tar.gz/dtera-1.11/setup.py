# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 20:36:58 2017

@author: a
"""

from distutils.core import setup
from setuptools import setup, find_packages, Extension
AUTHOR = "dtera"  
AUTHOR_EMAIL = "79845658@qq.com" 
setup(name='dtera',
      version='1.11',
      description='dtera',
      author=AUTHOR,  
      author_email=AUTHOR_EMAIL, 
      url='http://dtera.cn',
      ext_modules=[Extension('dtera',sources=['dtera.c'])],      
    )