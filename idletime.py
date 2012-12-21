#!/usr/bin/python

import ctypes


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
            raise Exception('Cannot open display')
        self.root = self.xlib.XDefaultRootWindow( self.dpy)
        self.xss = ctypes.cdll.LoadLibrary( 'libXss.so.1')
        self.xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
        self.xss_info = self.xss.XScreenSaverAllocInfo()

    def get_idle( self):
        self.xss.XScreenSaverQueryInfo( self.dpy, self.root, self.xss_info)
        return int(self.xss_info.contents.idle / 1000)

        
if __name__ == "__main__":
    s = XScreenSaverSession(":0")
    #t = XScreenSaverSession(":1")
    idle_time = s.get_idle()	
    print idle_time
	
     
