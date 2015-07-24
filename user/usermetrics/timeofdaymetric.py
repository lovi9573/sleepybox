#!/usr/bin/python
import suspendmetric
import datetime
import sys
import os
import subprocess
from PIL import Image
import StringIO
from ctypes import *


     

class Metric(suspendmetric.suspendmetric):
    
    def __init__(self,config):
        self.config = config
        super(Metric,self).__init__()
        

    def getSample(self):
        now = datetime.datetime.now()
        return now.hour+now.minute/60.0
    
    def getUnits(self):
        return "/24.00"
    
    def getFormatting(self):
        return ":2.2f"
    
        
