#!/usr/bin/python
import suspendmetric
import ctypes
import sys
import utility
import os
import subprocess
from PIL import Image
import StringIO


        

class Metric(suspendmetric.suspendmetric):
    
    def __init__(self,config):
        super(Metric,self).__init__(config.get('new_weight',1))
        self.sslib = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),'screenshot.so'))
        self.sslib.init()
        self.sslib.getPixelDiff.restype = ctypes.c_float
        

    def getSample(self,x):
        return self.sslib.getPixelDiff()
    
    def getUnits(self):
        return "/1.000"
    
    def getFormatting(self):
        return ":4.3f"
