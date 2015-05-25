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
    
    def __init__(self):
        self.lastScreenShots = {}

    def getMetric(self,x):
        return 10
        #im = Image.open(StringIO.StringIO("some image string"))
        displays = utility.getXSessionAuths()
        diff = 0
        d = 0
        for user,displayCreds in displays.items():
            os.environ['XAUTHORITY'] = displayCreds["xauthority"]
            os.environ['DISPLAY'] = displayCreds['display']
            TMPFILE = "/tmp/screenshot"+displayCreds['display']+".png"
            imagetext = subprocess.Popen(["scrot",TMPFILE], stdout=subprocess.PIPE).communicate()[0]
            image = Image.open(TMPFILE)
            flatimage = image.getdata()
            if(displayCreds['display'] in self.lastScreenShots.keys()):
                d = 0
                for  a,b in zip(self.lastScreenShots[displayCreds['display']],flatimage) :
                    if(a != b):
                        d += 1
            diff = max([diff,d])
            self.lastScreenShots[displayCreds['display']] = flatimage
        return diff
    
    def getUnits(self):
        return "px"
    
    def getFormatting(self):
        return ":>6"
