# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 13:34:18 2017

@author: Daniel
"""
import urllib.request
from zipfile import ZipFile
from asammdf import MDF

MDF(r'c:\Users\Daniel\Downloads\test.files\ASAP2_Demo_V161_2.00.mdf').convert('4.10').save(r'c:\Users\Daniel\Downloads\test.files\ASAP2_Demo_V161_2.00.mf4')