#!/usr/bin/python
import suspendmetric
import ctypes
import sys
import os
import subprocess


class XScreenSaverInfo(ctypes.Structure):
    """ typedef struct { ... } XScreenSaverInfo; """
    _fields_ = [('window',      ctypes.c_ulong), # screen saver window
                ('state',       ctypes.c_int),   # off,on,disabled
                ('kind',        ctypes.c_int),   # blanked,internal,external
                ('since',       ctypes.c_ulong), # milliseconds
                ('idle',        ctypes.c_ulong), # milliseconds
                ('event_mask',  ctypes.c_ulong)] # events

class XScreenSaverSession(object):
    def __init__( self,display_num):
        self.xlib = ctypes.cdll.LoadLibrary( '/usr/lib64/libX11.so.6')
        self.dpy = self.xlib.XOpenDisplay(display_num)
        if not self.dpy:
            raise Exception("Cannot open display " + display_num +"\n")
        self.root = self.xlib.XDefaultRootWindow( self.dpy)
        self.xss = ctypes.cdll.LoadLibrary( 'libXss.so.1')
        self.xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
        self.xss_info = self.xss.XScreenSaverAllocInfo()

    def get_idle( self):
        self.xss.XScreenSaverQueryInfo( self.dpy, self.root, self.xss_info)
        return int(self.xss_info.contents.idle / 1000)
    
    def close(self):
        if (self.xlib):
            self.xlib.XCloseDisplay(self.dpy)


class Metric(suspendmetric.suspendmetric):
    
    def __init__(self,config):
        #This metric class can be simplified since it is run for each user, who each know their own display number.
        self.config = config
        super(Metric,self).__init__()
        self.display = os.environ.get('DISPLAY',":0")
        self.session = XScreenSaverSession(self.display)

    def getSample(self):
        return self.session.get_idle()
    
    def getUnits(self):
        return "sec"
    
    def getFormatting(self):
        return ":4g"
        
if __name__ == "__main__":
    s = XScreenSaverSession(sys.argv[1])
    #t = XScreenSaverSession(":1")
    idle_time = s.get_idle()	
    print idle_time
	
     
