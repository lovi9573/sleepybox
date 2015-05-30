#!/usr/bin/python
import suspendmetric
import ctypes
import sys
import utility
import os
import subprocess
from PIL import Image
import StringIO


LIB='./metrics/screenshot.so'
        

class Metric(suspendmetric.suspendmetric):
    
    def __init__(self):
        self.sslib = ctypes.cdll.LoadLibrary(LIB)
        self.sslib.init()
        self.sslib.getPixelDiff.restype = ctypes.c_float
        

    def getMetric(self,x):
        return self.sslib.getPixelDiff()
    
    def getUnits(self):
        return "/1.00"
    
    def getFormatting(self):
        return ":>4"
