# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 16:50:39 2017

@author: Daniel
"""

from asammdf import MDF

MDF.merge([r'd:\PythonWorkspace\asammdf\benchmarks\test.mf4',] * 40, memory='low').save(r'd:\PythonWorkspace\asammdf\benchmarks\test_40.mf4')