#!/usr/bin/python
import suspendmetric
import ctypes
import sys
import utility
import os
import subprocess
from PIL import Image
import StringIO
from ctypes import *


        

class Metric(suspendmetric.suspendmetric):
    
    def __init__(self,config):
        self.config = config
        super(Metric,self).__init__()
        self.sslib = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),'screenshot.so'))
        self.sslib.init.restype = ctypes.c_int
        err = self.sslib.init()
        if err != 0:
            raise RuntimeError(str(err))
        self.sslib.getPixelDiff.restype = ctypes.c_int
        self.sslib.getPixelDiff.argtypes = [POINTER(c_float)]
        self.diff = ctypes.c_float()
        

    def getSample(self):
        err = self.sslib.getPixelDiff(ctypes.byref(self.diff))
        if err != 0:
            raise RuntimeError("error#:"+str(err))
        return self.diff
    
    def getUnits(self):
        return "/1.000"
    
    def getFormatting(self):
        return ":4.3f"
    
        
