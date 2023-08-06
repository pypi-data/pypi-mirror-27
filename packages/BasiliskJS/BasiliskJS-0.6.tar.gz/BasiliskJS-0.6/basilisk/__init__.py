#!/usr/bin/python3
# coding: utf8

__author__ = 'lich666dead'
__title__ = 'BasiliskJS'
__version__ = '0.6'
__copyright__ = 'Copyright 2017 lich666dead'


try:
    from .basilisk import PhantomJS
except:
    from basilisk import PhantomJS
